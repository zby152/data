%水印嵌入
%W_SVD_hide("Lena.jpg",'db6',2,0.99,10,0.5)   调用例子
function W_SVD_hide(image_path,wavelet,N,ratio,seed,alpha)

% image_path="Lena.jpg";
% wavelet='db6';     %使用的小波函数
% N=2;                %小波分解的层数
% ratio=0.99;
% seed=10;
% alpha=0.5;

%规定文件的输出路径以及stirmark指定文件夹的路径
output_path='lenna-waved.jpg';
target_path='E:\matlab_codes\lab_3\stirmark\Media\Input\Images\Set1';

%取出图像的三个色域，只取R层进行水印嵌入
image=imread(image_path);
image= double(image)/255; 
R=image(:,:,1);
G=image(:,:,2);
B=image(:,:,3);

%对图像的R层进行小波分解，得到C为各层分解系数,s_real为未补足的各层分解系数长度
[C,S_real]=wavedec2(R,N,wavelet);

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

%将分解得到的矩阵后面的部分替换
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

%只选取有信息的部分
if high <= width   
    waterCA = waterCA(1:S_real(1,1),:) ;
else
    waterCA = waterCA(:,1:S_real(1,2) ) ;
end 

% 重构带有水印的低频系数矩阵并用其替换C
CA_tilda = reshape( CA_tilda, 1, S( 1, 1) * S( 1,2) ) ;
C( 1, 1:S( 1, 1) * S( 1, 2) ) = CA_tilda;

%将带有水印的C进行逆小波变换，还原成原图像的格式
watermarkimage = waverec2( C, S, wavelet) ; 

% 将前面补上的边缘去掉
if high <= width  
    watermarkimage = watermarkimage( 1:high,:) ;
else
    watermarkimage = watermarkimage(:, 1:width) ;
end

%得到嵌入水印后的图像并写入目标位置
watermarkimage_rgb=cat(3,watermarkimage,G,B);
imwrite( watermarkimage_rgb, output_path) ;

%将嵌入水印后的图像复制到stirmark工具对应文件夹中
copyfile(output_path,target_path);

%输出结果
figure(1) ; 
subplot( 223) ; imshow( watermark*255) ; title('水印模板' ) ; 
subplot( 221) ; imshow(image) ; title( ' 原始图像' ) ; 
subplot( 222) ; imshow( watermarkimage_rgb) ; title( '嵌入水印后的图像' ) ; 