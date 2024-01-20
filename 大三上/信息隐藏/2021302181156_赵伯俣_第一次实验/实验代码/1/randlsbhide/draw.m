%原图
f=imread('Lena.bmp');%读入图片
[ m, n] = size(f) ;
result_1= zeros(1, 256);
for i=1:m
    for j=1:n
        for k=1:256
            if f(i,j)-1==k
                result_1(k)=result_1(k)+1;
            end
        end
    end
end

result=0;
for x=1:255
    y=x+1;
    result=result+abs(result_1(x)-result_1(y));
end
subplot(211),imhist(f),title("隐写之前的文件");
axis([0 255 0 6000]);%设置x、y轴坐标范围 

%隐写后图像
f2=imread('scover.bmp');%读入图片
result_2= zeros(1, 256);
for i=1:m
    for j=1:n
        for k=1:256
            if f2(i,j)-1==k
                result_2(k)=result_2(k)+1;
            end
        end
    end
end

result2=0;
for x=1:255
    y=x+1;
    result2=result2+abs(result_2(x)-result_2(y));
end

subplot(212),imhist(f2),title("隐写之后的文件");
axis([0 255 0 6000]);%设置x、y轴坐标范围 

