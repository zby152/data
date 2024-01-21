image_path="lena.png";    %载体图像
scover_path="F5_scover.png";    %隐写后输出载密图像
message_path="message.txt";

%位置置乱函数参数
times=10;     %置乱次数
c_a=3;
c_b=5;

%读取秘密信息
f_id = fopen(message_path, "r") ;
[ msg,len_total] = fread( f_id, 'ubit1') ;
data_len=len_total/3;

%读取载体图像，只取其红色部分进行隐写
image=imread(image_path);
R=image(:,:,1);
G=image(:,:,2);
B=image(:,:,3);
cover=R;

% 标准量化表
Q=[16 11 10 16 24 40 51 61
   12 12 14 19 26 58 60 55
   14 13 16 24 40 57 69 56
   14 17 22 29 51 87 80 62
   18 22 37 56 68 109 103 77
   24 35 55 64 81 104 113 92
   49 64 78 87 103 121 120 101
   72 92 95 98 112 100 103 99];

%汉明码一致校验矩阵
M=[0 0 0 1 1 1 1
   0 1 1 0 0 1 1
   1 0 1 0 1 0 1];   

% 初始化，DCT转换和量化
[h,w]=size(cover);
D=zeros(h,w);           %零时存储矩阵
for i=1:h/8
    for j=1:w/8
        D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=dct2(cover(8*(i-1)+1:8*i,8*(j-1)+1:8*j));
        D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=round(D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)./Q);
    end
end

%位置置乱操作
%figure(1);imshow(D)
N=h;
D2=zeros(h,w);
for i=1:times
    for x=1:h
        for y=1:w           
            xx=mod((x-1)+c_b*(y-1),N)+1;   %mod(a,b)就是a除以b的余数
            yy=mod(c_a*(x-1)+(c_a*c_b+1)*(y-1),N)+1;        
            D2(yy,xx)=D(y,x);                
        end
    end
    D=D2;
end
%figure(2);imshow(D);

% 隐写
stego=D;
num=1;          %记录目前已经嵌入的data数量
a=zeros(7,1);   %记录隐写载体的7个可隐写位
k=1;            %记录当前7个数值中已取数量
sit=zeros(7,2); %记录当前7个数在载体中的位置
change=0;       %记录发生修改的次数

for i=1:h
    for j=1:w
        if (mod(i-1,8)~=0 || mod(j-1,8)~=0) && (i~=1 || j~=1)
            if (D(i,j)>0 && mod(D(i,j),2)==1)||(D(i,j)<0 && mod(D(i,j),2)==0)        %正奇数或负偶数为1
                a(k)=1;
                sit(k,1)=i;
                sit(k,2)=j;
                k=k+1;
            elseif (D(i,j)<0 && mod(D(i,j),2)==1)||(D(i,j)>0 && mod(D(i,j),2)==0)    %负奇数或正偶数为0
                a(k)=0;
                sit(k,1)=i;
                sit(k,2)=j;
                k=k+1;
            end
        end

        %当有7个隐写载体可隐写位时
        if(k>7)
            %据算出n的值，n为要修改的位数
            data_bit=[msg(num*3-2);msg(num*3-1);msg(num*3)];  
            temp=M*a;
            temp=mod(temp,2);
            n=bitxor(data_bit,temp);      %按位异或
            n=n(1)*4+n(2)*2+n(3);

            % 修改第n位的DCT值
            if n>0
                if D(sit(n,1),sit(n,2))<0
                    stego(sit(n,1),sit(n,2))=D(sit(n,1),sit(n,2))+1;
                    change=change+1;
                elseif D(sit(n,1),sit(n,2))>0
                    stego(sit(n,1),sit(n,2))=D(sit(n,1),sit(n,2))-1;
                    change=change+1;
                end

                % 检查修改过后的DCT值是否为0，若为0则重新选择1位数据作为载体信号
                if stego(sit(n,1),sit(n,2))==0
                    k=k-1;
                    sit(n:k-1,:)=sit(n+1:k,:);
                    a(n:k-1)=a(n+1:k);
                    continue;
                end
            end
            num=num+1;
            k=1;
        end
        if(num>data_len)
            break;
        end
    end
    if(num>data_len)
        break;
    end
end

%位置置乱还原
%figure(3);imshow(stego);
stego2=stego;
for i=1:times
    for x=1:h
        for y=1:w            
            xx=mod((c_a*c_b+1)*(x-1)-c_b*(y-1),N)+1;
            yy=mod(-c_a*(x-1)+(y-1),N)+1  ;        
            stego2(yy,xx)=stego(y,x);                   
        end
    end
    stego=stego2;
end
%figure(4);imshow(stego);

% 逆DCT转换，转换成伪装图像
for i=1:h/8
    for j=1:w/8
        stego(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=stego(8*(i-1)+1:8*i,8*(j-1)+1:8*j).*Q;
        stego(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=idct2(stego(8*(i-1)+1:8*i,8*(j-1)+1:8*j));
    end
end

%隐写后图像与其余两个颜色部分混合后保存
Mix=cat(3,stego,G,B);
imwrite(Mix,scover_path);

figure(5);
subplot(1,2,1),imshow(image),title('原图');
subplot(1,2,2),imshow(Mix),title('嵌入信息后的图像');




