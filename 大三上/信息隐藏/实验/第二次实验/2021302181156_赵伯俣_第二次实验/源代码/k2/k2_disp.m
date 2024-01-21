image="scover_LSBM.bmp";
%image="scover_LSBR.bmp";
%image="F4_scover.png";
%image="F5_scover.png";

%读取图像信息若为png图片则只取其红色部分
ste_cover=imread(image); 
ste_cover=ste_cover(:,:,1);

[m,n]=size(ste_cover); 

%存放每一份图像的卡方统计量和被隐写概率
S=[];
P_values=[];

%将图像按10%的分割，一共分成10份
part=m/10;

%统计每一个10%的卡方统计量
for j=0:9
    h=imhist(ste_cover(floor(j* part)+1:floor((j+1)* part),:));
    h(1) = 0;
    h(2) = 0;
    h_length=size(h);
    p_num=floor(h_length/2);   
    Spov=0; %记录卡方统计量
    K=0;
    for i=1:p_num
        if(h(2*i-1)+h(2*i))~=0
            Spov=Spov+(h(2*i-1)-h(2*i))^2/(2*(h(2*i-1)+h(2*i))); 
            K=K+1;
        end
    end
    %Spov为卡方统计量，K-1为自由度
    P=1-chi2cdf(Spov,K-1);   
    
    if j~=0
      Spov=Spov+S(j); %若不注释则为累计卡方统计量 
    end
    
    S=[S Spov];
    P_values=[ P_values P];
end

%显示变化曲线，x_label是横坐标，代表分析样本占整幅图像的百分比
x_label=0.1:0.1:1;
figure,
plot(x_label,P_values,'LineWidth',2),title('p值与分析图像的像素比例关系');
xlabel('分析图像的像素比例');
ylabel('p值');
ylim([0, 1])

