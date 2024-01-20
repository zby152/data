%randlsbget( 'scover.bmp', 168, 'secret.txt', 2001)
function result = randlsbget( output, len_total, goalfile, key)
ste_cover = imread( output) ;
ste_cover = double( ste_cover) ;

frr = fopen( goalfile, 'a') ;
% p 代表提取进度
p = 1;
% 调用随机间隔函数选取像素点
[ row, col] = randinterval( ste_cover, len_total, key);
for i = 1:len_total
    if bitand( ste_cover( row( i) , col( i) ) , 1) == 1
        fwrite( frr, 1, 'ubit1') ;
        result( p, 1 ) = 1;
    else
        fwrite( frr, 0, 'ubit1') ;
        result( p, 1 ) = 0;
    end
    if p == len_total
        break;
    end
    p = p + 1;
end
fclose( frr) ;