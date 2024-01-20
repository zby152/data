%%批量计算各个参数的不同所绘制出的相关性SC图
%原图路径和待测图像路径
image_origin_path='Lena.jpg';
image_test_path='lenna-waved.jpg';

%初始化检测参数
seed_real=10;
N_real=2;
ratio_real=0.99;
wavelet_real='db6';
alpha_real=0.5;

N=N_real;
ratio=ratio_real;
wavelet=wavelet_real;
alpha=alpha_real;

%% 分析种子值的不同
%选定种子值的选取范围
seeds=[2,4,6,8,10,12,14,16,18,20];

%保存检测结果
corr_seed=[];
corr_DCT_seed=[];

%对每一个选定的种子值计算相关性并保存
for index=1:10
    seed=seeds(index);
    [corr,corr_DCT]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha);
    corr_seed=[corr_seed,corr];
    corr_DCT_seed=[corr_DCT_seed,corr_DCT];
end

%调用函数绘制SC图
disp_xy(seeds,corr_seed,corr_DCT_seed,'关于种子的小波系数阈值分析','种子',0);
%恢复种子值
seed=seed_real;

%% 分析小波变换次数的不同
Ns=[1,2,3,4,5,6,7,8];
corr_N=[];
corr_DCT_N=[];

for index=1:8
    N=Ns(index);
    [corr,corr_DCT]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha);
    corr_N=[corr_N,corr];
    corr_DCT_N=[corr_DCT_N,corr_DCT];
end

disp_xy(Ns,corr_N,corr_DCT_N,'关于小波变换次数的小波系数阈值分析','小波变换次数',0);
N=N_real;

%% 分析替换比例的不同
ratios=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99];
corr_ratio=[];
corr_DCT_ratio=[];

for index=1:10
    ratio=ratios(index);
    [corr,corr_DCT]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha);
    corr_ratio=[corr_ratio,corr];
    corr_DCT_ratio=[corr_DCT_ratio,corr_DCT];
end

disp_xy(ratios,corr_ratio,corr_DCT_ratio,'关于替换比例的小波系数阈值分析','替换比例',0);
ratio=ratio_real;

%% 分析使用小波函数种类的不同
wavelets=["haar","db1","db6","db10","db45","coif1","coif2"];
corr_wavelet=[];
corr_DCT_wavelet=[];

for index=1:7
    wavelet=wavelets(1,index);
    [corr,corr_DCT]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha);
    corr_wavelet=[corr_wavelet,corr];
    corr_DCT_wavelet=[corr_DCT_wavelet,corr_DCT];
end

disp_xy(wavelets,corr_wavelet,corr_DCT_wavelet,'关于小波函数种类的小波系数阈值分析','小波函数种类',1);
wavelet=wavelet_real;

%% 分析生成随机对角矩阵参数的不同
alphas=[0,0.1,0.2,0.3,0.4,0.5,0.6];
corr_alpha=[];
corr_DCT_alpha=[];

for index=1:7
    alpha=alphas(index);
    [corr,corr_DCT]=W_SVD_find(image_origin_path,image_test_path,wavelet,N,ratio,seed,alpha);
    corr_alpha=[corr_alpha,corr];
    corr_DCT_alpha=[corr_DCT_alpha,corr_DCT];
end

disp_xy(alphas,corr_alpha,corr_DCT_alpha,'关于生成随机对角矩阵参数的小波系数阈值分析','生成随机对角矩阵参数',0);