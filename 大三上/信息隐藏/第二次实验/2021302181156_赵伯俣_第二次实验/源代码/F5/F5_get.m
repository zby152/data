image_name="F5_scover.png";    %隐写后图像
len_total=840;                 %提取的比特长度
result_path="result.txt";

%位置置乱参数
times=10;    %置乱次数
c_a=3;
c_b=5;

data_len=len_total/3;  %每三个比特分一组，总的组数

%读取载体图像，只取其红色部分进行提取
image=imread(image_name);
R=image(:,:,1);
G=image(:,:,2);
B=image(:,:,3);
stego=R;

% 初始化标准量化表
Q=[16 11 10 16 24 40 51 61
   12 12 14 19 26 58 60 55
   14 13 16 24 40 57 69 56
   14 17 22 29 51 87 80 62
   18 22 37 56 68 109 103 77
   24 35 55 64 81 104 113 92
   49 64 78 87 103 121 120 101
   72 92 95 98 112 100 103 99];

[h,w]=size(stego);

%汉明码一致校验矩阵
M=[0 0 0 1 1 1 1
   0 1 1 0 0 1 1
   1 0 1 0 1 0 1];   

D=zeros(h,w);

% DCT转换和量化
for i=1:h/8
    for j=1:w/8
        D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=dct2(stego(8*(i-1)+1:8*i,8*(j-1)+1:8*j));
        D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)=round(D(8*(i-1)+1:8*i,8*(j-1)+1:8*j)./Q);
    end
end

% 位置置乱
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

% 数据提取
num=1;          %记录目前已经嵌入的data数量
a=zeros(7,1);
k=1;            %记录当前7个数值中已取数量
result=zeros(len_total,1);

for i=1:h
    for j=1:w
        %取得隐写后载体a的7位值
        if (mod(i-1,8)~=0 || mod(j-1,8)~=0) && (i~=1 || j~=1)
            if (D(i,j)>0 && mod(D(i,j),2)==1)||(D(i,j)<0 && mod(D(i,j),2)==0)        %正奇数或负偶数为1
                a(k)=1;
                k=k+1;
            elseif (D(i,j)<0 && mod(D(i,j),2)==1)||(D(i,j)>0 && mod(D(i,j),2)==0)    %负奇数或正偶数为0
                a(k)=0;
                k=k+1;
            end
        end

        %表示集满7个数据
        if k>7  
            temp=M*a;
            temp=mod(temp,2);
            result(num*3-2)=temp(1);
            result(num*3-1)=temp(2);
            result(num*3)=temp(3);
            num=num+1;
            k=1;
        end
        if num>data_len
            break;
        end
    end
    if num>data_len
        break;
    end
end

%提取到的秘密信息写入文件
frr = fopen(result_path, 'a');
for x=1:len_total
    if result(x)==0
        fwrite( frr, 0,'ubit1') ;
    else
        fwrite( frr, 1,'ubit1') ;
    end
end








