input="Lena.bmp";   %隐写载体
output="scover_LSBR.bmp";    %生成载密图像
k=0.9;  %嵌入率

cover = imread(input) ;
ste_cover = cover;
ste_cover = double( ste_cover) ;

[ m, n] = size( ste_cover) ;

%按照嵌入率的大小随机生成生成对应的秘密信息01矩阵
x=round(m*k);
msg=randsrc(x,n,[0 1;0.5 0.5]);
writematrix(msg,"message.txt");

change=0;     %统计嵌入信息时的修改次数

% 在 LSB位隐写
for i = 1:x
    for j=1:n
        change=change+1;
        ste_cover(i,j) = ste_cover(i,j) -mod( ste_cover(i,j) , 2) + msg(i,j);
    end  
end

% 隐写后的图像输出
ste_cover = uint8( ste_cover) ;
imwrite( ste_cover, output) ;

% 显示实验结果
subplot( 2, 2, 1) ; imshow( cover) ; title( "原始图像") ;
subplot( 2, 2, 2) ; imshow( ste_cover) ; title("隐藏信息的图像") ;
subplot( 2, 2, 3) ; imhist( cover) ; title( "原始图像直方图") ;
subplot( 2, 2, 4) ; imhist( ste_cover) ; title("隐藏信息的图像直方图") ;






