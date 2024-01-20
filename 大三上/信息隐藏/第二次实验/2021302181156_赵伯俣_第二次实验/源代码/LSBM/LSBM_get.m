input="scover_LSBM.bmp";    %隐写后图像
goalfile="result.txt";    %提取信息存放位置
k=0.9;                    %嵌入率

ste_cover = imread( input) ;
[m,n] = size( ste_cover) ;
x=round(m*k);

len_total=x*n;
result=zeros(x,n);

%p代表提取信息的个数
p = 1;
for i = 1:x
    for j = 1:n
        if mod( ste_cover( i, j) , 2) == 1
            result(i,j)=1;
        else
            result(i,j)=0;
        end
        if p == len_total
            break;
        end
        p = p + 1;
    end
    if p == len_total
        break;
    end
end

%将提取得到的信息写入文件
writematrix(result,goalfile);