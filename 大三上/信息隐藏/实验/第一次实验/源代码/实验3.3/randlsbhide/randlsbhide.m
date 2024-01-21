%randlsbhide ('Lena.bmp','m.txt', 'scover.bmp', 2001 )
function [ ste_cover, len_total] = randlsbhide( input, file, output, key)
% 读入图像矩阵
cover = imread( input) ;
ste_cover = cover;
ste_cover = double( ste_cover) ;
% 将文本文件转换为二进制
f_id = fopen( file, "r") ;
[ msg,len_total] = fread( f_id, 'ubit1') ;
% 判断嵌入消息量是否过大
[ m, n] = size( ste_cover) ;
if len_total > m*n
    error( "嵌入消息量过大, 请更换图像") ;
end
% p 表示当前隐写到的bit位数
p = 1;
% 调用随机间隔函数选取像素点
[ row, col] = randinterval( ste_cover, len_total, key) ;

% 在 LSB 隐秘消息
for i = 1:len_total
    ste_cover(row( i) , col( i) ) = ste_cover(row(i) , col(i))-mod( ste_cover(row(i) , col(i)),2)+ msg(p,1) ;
    if p == len_total
        break;
    end
    p = p + 1;
end

% 隐写后的图像输出
ste_cover = uint8( ste_cover) ;
imwrite( ste_cover, output) ;

% 显示实验结果
subplot( 1, 2, 1) ; imshow( cover) ; title( "原始图像") ;
subplot( 1, 2, 2) ; imshow( output) ; title("隐藏信息的图像") ;
