%计算原图与待测图片的相关性
%W_SVD_find('Lena.jpg','lenna-waved.jpg','db6',2,0.99,10,0.5)
function [corr_coef,corr_DCTcoef]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha)

% image_origin_path='Lena.jpg';
% image_test_path='lenna-waved.jpg';
% wavelet='db6';     %使用的小波函数
% N=2;                %小波分解的层数
% ratio=0.99;
% seed=10;
% alpha=0.5;
%提取原图的R层
image_origin=imread(image_origin_path);
image_origin=double(image_origin)/255;
R_origin=image_origin(:,:,1);

%提取测试图像的R层
image_test=imread(image_test_path);
image_test=double(image_test)/255;
R_test=image_test(:,:,1);

%提取出原图带有水印的小波系数
[waterCA_origin]=W_SVD_get_waterCA(image_origin_path,wavelet,N,ratio,seed,alpha);

%提取原图的小波系数
[C_origin,S_origin]=wavedec2(R_origin,N,wavelet);
CA_origin = appcoef2(C_origin,S_origin,wavelet,N);
%提取待测图像的小波系数
[C_test,S_test]=wavedec2(R_test,N,wavelet);
CA_test = appcoef2(C_test,S_test,wavelet,N);

%生成原始水印
watermark_origin=waterCA_origin-CA_origin;
%提取出待测水印
watermark_test=CA_test-CA_origin;

%计算相关性
corr_coef=trace(watermark_origin'*watermark_test)/(norm(watermark_origin,'fro')*norm(watermark_test,'fro'));

%取原图和待检测图像的DCT系数
DCTrealwm=dct2(watermark_origin);
DCTtestwm=dct2(watermark_test);

%取出原图和待检测图像32*32块的DCT系数
DCTrealwm=DCTrealwm(1:min(32,max(size(DCTrealwm))),1:min(32,max(size(DCTrealwm))));
DCTtestwm=DCTtestwm(1:min(32,max(size(DCTtestwm))),1:min(32,max(size(DCTtestwm))));

%计算相关性
corr_DCTcoef=trace(DCTrealwm'*DCTtestwm)/(norm(DCTrealwm,'fro')*norm(DCTtestwm,'fro'));