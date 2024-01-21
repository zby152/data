input_path='F4_scover.png';   %载密图像位置
result_path='result.txt';
len_total=840;

%读取图像后只取R层进行提取
A=imread(input_path);
R=A(:,:,1);
G=A(:,:,2);
B=A(:,:,3);
I=R;

[m,n]=size(R);

frr = fopen(result_path, 'a');

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

%提取
x=1;  %当前处理的字节指针
msg=zeros(len_total,1);
for i=1:m
    for j=1:n
        if x<=len_total && (mod(i-1,8)~=0 || mod(j-1,8)~=0) &&(i~=1 || j~=1) %只取LSB位
            ac=jpeg_img(i,j);
            if ac~=0   %去掉0
                if ac>0
                    if mod(ac,2)==0
                        fwrite( frr, 0,'ubit1') ;
                        msg(x)=0;
                    else
                        fwrite( frr, 1,'ubit1') ;
                        msg(x)=1;
                    end
                else
                    if mod(ac,2)==0
                        fwrite( frr, 1,'ubit1') ;
                        msg(x)=1;
                    else
                        fwrite( frr, 0,'ubit1') ;
                        msg(x)=0;
                    end
                end
                x=x+1;

            end
        end
    end
end
fclose(frr) ;

