%取水印嵌入函数的前部分，但不将水印嵌入后的图片写入文件只得到小波系数
function [waterCA]=W_SVD_get_waterCA(image_path,wavelet,N,ratio,seed,alpha)

% image_path="Lena.jpg";
% wavelet='db6';     %使用的小波函数
% N=2;                %小波分解的层数
% ratio=0.99;
% seed=10;
% alpha=0.5;

image=imread(image_path);
image= double(image)/255; 
R=image(:,:,1);

%将原始图像补足成正方形
[high,width]=size(R);
max_size=max(high,width);
cover=zeros(max_size);
if high <= width  
    cover( 1:high,:) = R;
else
    cover(:,1:width) = R;
end 

%补足后的图像小波分解
[C,S]=wavedec2(cover,N,wavelet);
%提取N级低频成分保存到CA中
CA = appcoef2(C,S,wavelet,N);

%对低频小波系数归一化处理，对原始数据的线性变换，使结果值映射到[0 - 1]之间
CAmin = min(min(CA)) ;
CAmax = max(max(CA)) ;
CA=(1/(CAmax-CAmin))*(CA-CAmin);

d=max(size(CA));
%对低频系数进行单值分解
[U,sigma,V]=svd(CA);

%计算水印容量,替换的比例
np = round(d*ratio); 

%按照种子生成随机矩阵
rand('seed', seed)

%生成两个随机正交矩阵Q_V,Q_U
M_V = rand( d, np) - 0.5;       %rand生成的随机矩阵均值为0.5
[ Q_V, R_V] = qr( M_V, 0) ;     %将矩阵M分解成正交矩阵Q和上三角矩阵R
M_U = rand( d, np) - 0.5;
[ Q_U, R_U] = qr( M_U, 0) ;

%将后面的部分替换
V2 = V; 
U2 = U; 
V(:, d - np +1: d) = Q_V(:, 1: np) ; 
U(:, d - np +1: d) = Q_U(:, 1: np) ;

%生成随机对角矩阵
sigma_tilda = alpha* flipud(sort( rand( d, 1))) ; 

% 生成水印模板
watermark = U* diag( sigma_tilda, 0) * V ; 

% 调整系数生成嵌入水印后的图像，将过幅系数与负数修正 
CA_tilda = CA + watermark;
over1 = find( CA_tilda > 1) ;
below0 = find( CA_tilda < 0) ;
CA_tilda(over1) = 1;
CA_tilda(below0) = 0; 

%系数还原到归一化以前的范围 
CA_tilda = ( CAmax-CAmin) * CA_tilda +CAmin; 

%加有水印的低频系数
waterCA = CA_tilda;
