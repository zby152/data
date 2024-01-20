input="Lena.bmp";   %隐写载体
output="scover_LSBM.bmp";    %隐写后图像保存位置
k=0.9;  %嵌入率

cover = imread(input) ;
ste_cover = cover;
ste_cover = double( ste_cover) ;

[ m, n] = size( ste_cover) ;

%按照嵌入率生成对应数量的秘密信息
x=round(m*k);
msg=randsrc(x,n,[0 1;0.5 0.5]);
writematrix(msg,"message.txt");

change=0;     %记录隐写时修改的次数

% 在 LSB位进行隐写
for i = 1:x
    for j=1:n
        if mod(ste_cover(i,j),2)~=msg(i,j)
            change=change+1;
            if ste_cover(i,j)==0
                ste_cover(i,j)=1;
            elseif ste_cover(i,j)==255
                ste_cover(i,j)=254;
            else
                ste_cover(i,j)=plus_or_sub(ste_cover(i,j));
            end
        end
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






