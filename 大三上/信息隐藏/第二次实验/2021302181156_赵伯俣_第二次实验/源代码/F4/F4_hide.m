input_path='lena.png';
output_path='F4_scover.png';

%读取隐写载体的红色部分
A=imread(input_path);
R=A(:,:,1);
G=A(:,:,2);
B=A(:,:,3);

[m,n]=size(R);

%获取隐藏信息的二进制数据
f_id = fopen("message.txt", "r") ;
[ msg,len_total] = fread( f_id, 'ubit1') ;

%只取R层进行隐写
I =R;

%量化矩阵
mask1=[16 11 10 16 24 40 51 61
       12 12 14 19 26 58 60 55
       14 13 16 24 40 57 69 56
       14 17 22 29 51 87 80 62
       18 22 37 56 68 109 103 77
       24 35 55 64 81 104 113 92
       49 64 78 87 103 121 120 101
       72 92 95 98 112 100 103 99];

% 将图像进行jepg压缩
jpeg_img=zeros(m,n);
for row=1 :8:m
    for col= 1:8:n
        DCT_matrix=I(row:row+7,col:col+7); 
        %将每一块进行DCT变换
        DCT_matrix=dct2(DCT_matrix);  
        %将每一块通过矩阵进行量化
        DCT_matrix=round(DCT_matrix./mask1); 
        %将量化后的块写入jpeg_img
        jpeg_img(row:row+7,col:col+7)=DCT_matrix;
    end
end

%显示隐写前的DCT系数直方图
subplot(2,2,3),histogram(jpeg_img),title('经过隐写前的DCT系数图');
%subplot(2,1,1),histogram(jpeg_img),title('经过隐写前的DCT系数图');

%隐写
change=0;    %记录修改载体次数5
x=1;  %当前处理的字节指针
for i=1:m
    for j=1:n
        if x<=len_total && (mod(i-1,8)~=0 || mod(j-1,8)~=0) && (i~=1 || j~=1)   %只取LSB位
            ac=jpeg_img(i,j);
            if ac~=0 %去掉0
                if mod(ac,2)==0
                    if ac>=0
                        if msg(x)==1
                            ac=ac-1;
                        end
                    else
                        if msg(x)==0
                            ac=ac+1;
                        end
                    end
                else
                    if ac>=0
                        if msg(x)==0
                            ac=ac-1;
                        end
                    else
                        if msg(x)==1
                            ac=ac+1;
                        end
                    end
                end
                jpeg_img(i,j)=ac;
                change=change+1;
                %若修改后ac系数为0则重新对该位进行隐写
                if ac~=0
                    x=x+1;
                end
            end
        end
    end
end

%显示隐写之后的DCT系数直方图
subplot(2,2,4),histogram(jpeg_img),title('经过隐写后的DCT系数图');
%subplot(2,1,2),histogram(jpeg_img),title('经过隐写后的DCT系数图');

% 逆DCT变换
for row=1:8:m
    for col=1:8:n
        IDCT_matrix=jpeg_img(row:row+7,col:col+7);
        IDCT_matrix=round(idct2(IDCT_matrix.*mask1)); 
        recon_img(row:row+7,col:col+7)=IDCT_matrix;
    end
end

%将三个颜色部分混合
Mix=cat(3,recon_img,G,B);
imwrite(Mix,output_path);

figure(1);
subplot(2,2,1),imshow(A),title('原图');
subplot(2,2,2),imshow(Mix),title('嵌入信息');

