%对于嵌入水印后的图片攻击后，对于每种攻击方式进行分析
%原图路径
origin_path='Lena.jpg';

%设置每一种攻击方式中的下标
number1=[0,20,40,60,80,100];
number2=[3,5,7,9];
number3=[30,40,50,60,70,80,90,100];

%选定攻击方式,修改n的值和numbers选用的数组
n=2;
numbers=number2;

%选定小波变换参数
seed=10;
N=2;
ratio=0.99;
wavelet='db6';
alpha=0.5;

%定义攻击方式
ways=["NOISE","MEDIAN","JPEG"];
way=char(ways(1,n));

% 攻击后产生的图片的存放位置
file_path =['E:\matlab_codes\lab_3\stirmark\Media\Output\Images\Set1\',way,'\'];

%保存选定文件夹所有图片的信息
img_path_list = dir(strcat(file_path,'lenna-waved_',way,'_*.bmp'));

%图像总数量
img_num = length(img_path_list);

if img_num > 0 
    corrs=[];
    corr_DCTs=[];
    for j = 1:img_num %逐一读取图像
        img_name = [file_path,'lenna-waved_',way,'_',num2str(numbers(j)),'.bmp'];
        [corr,corr_DCT]=W_SVD_find(origin_path,img_name,wavelet,N,ratio,seed,alpha);
        corrs=[corrs,corr];
        corr_DCTs=[corr_DCTs,corr_DCT];
    end
    disp_xy(numbers,corrs,corr_DCTs,'中值滤波攻击下检测出的相关性','中值滤波攻击参数',0);
end
