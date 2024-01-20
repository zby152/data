function [count_false] = dcthide2(a)

count_false=0;
A=imread('lena.png');
R=A(:,:,1);
G=A(:,:,2);
B=A(:,:,3);
f_id = fopen("m.txt", "r") ;
[ msg,len_total] = fread( f_id, 'ubit1') ;

%隐写
I = im2double(R);
D = dctmtx(8);%生成变换矩阵
C = blkproc(I,[8,8],'P1*x*P2',D,D');
mask1=[16 11 10 16 24 40 51 61
    12 12 14 19 26 58 60 55
    14 13 16 24 40 57 69 56
    14 17 22 29 51 87 80 62
    18 22 37 56 68 109 103 77
    24 35 55 64 81 104 113 92
    49 64 78 87 103 121 120 101
    72 92 95 98 112 100 103 99];

C = blkproc(C,[8,8],'x./P1',mask1);%量化
[m,n]=size(C);
u=[5 2];%[2 3]
v=[4 3];%[4 1]

x=1;  %当前处理的字符指针
len_total; %隐写信息长度
capacity=m*n/64;

if len_total>capacity
    disp('隐藏信息过多');
    exit;
end

%隐藏
for i=1:8:m
    for j=1:8:n
        if x<=len_total
            if msg(x)==1     %隐写信息1 调整v的部分比u大一个a
                if C(i+u(1)-1,j+u(2)-1) > C(i+v(1)-1,j+v(2)-1)
                    medium=C(i+u(1)-1,j+u(2)-1)+a;
                    C(i+u(1)-1,j+u(2)-1)=C(i+v(1)-1,j+v(2)-1);
                    C(i+v(1)-1,j+v(2)-1)=medium;
                    x=x+1;
                elseif C(i+u(1)-1,j+u(2)-1)==C(i+v(1)-1,j+v(2)-1)
                    C(i+v(1)-1,j+v(2)-1)=C(i+v(1)-1,j+v(2)-1)+a;
                    x=x+1;
                else
                    x=x+1;
                    continue;
                end
            elseif msg(x)==0    %隐写信息0
                if C(i+u(1)-1,j+u(2)-1)<C(i+v(1)-1,j+v(2)-1)
                    medium=C(i+u(1)-1,j+u(2)-1);
                    C(i+u(1)-1,j+u(2)-1)=C(i+v(1)-1,j+v(2)-1)+a;
                    C(i+v(1)-1,j+v(2)-1)=medium;
                    x=x+1;
                elseif C(i+u(1)-1,j+u(2)-1)==C(i+v(1)-1,j+v(2)-1)
                    C(i+u(1)-1,j+u(2)-1)=C(i+u(1)-1,j+u(2)-1)+a;
                    x=x+1;
                else
                    x=x+1;
                    continue;
                end
            end
        else
            break;
        end
    end
end
C = blkproc(C,[8,8],'x.*P1',mask1);
%图像重构
C = blkproc(C,[8,8],'P1*x*P2',D',D);
figure(1)
C=im2uint8(C);
Mix=cat(3,C,G,B);

imwrite(C,"scover.bmp");
subplot(1,2,1),imshow(A),title('原图');
subplot(1,2,2),imshow(Mix),title('嵌入信息');

%提取
R=Mix(:,:,1);
G=Mix(:,:,2);
B=Mix(:,:,3);
img=im2double(R);
img = blkproc(img,[8,8],'P1*x*P2',D,D');
s=1; %当前提取到的bit个数
frr = fopen("result.txt", 'a');

for i=1:8:m
    for j=1:8:n
        if s<=len_total
            if img(i+u(1)-1,j+u(2)-1)>img(i+v(1)-1,j+v(2)-1)
                fwrite( frr, 0,'ubit1') ;
                result_msg(s)=0;
                s=s+1;
            elseif img(i+u(1)-1,j+u(2)-1)<img(i+v(1)-1,j+v(2)-1)
                fwrite( frr, 1, 'ubit1') ;
                result_msg(s)=1;
                s=s+1;
            end
        else
            break;
        end
    end
end
fclose(frr) ;

%输出误码率
for i=1:len_total
    if result_msg(i) ~= msg(i)
        count_false=count_false+1;
    end
end
