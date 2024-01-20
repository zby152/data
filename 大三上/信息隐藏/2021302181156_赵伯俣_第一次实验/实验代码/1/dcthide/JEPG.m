%%
%压缩
X=blkproc(C,[8,8],'P1*x*P2',D,D');%DCT
X = blkproc(X,[8,8],'x./P1',mask1);%量化
X=X*100000;
X=floor(X);
X=X/100000;
X1= blkproc(X,[8,8],'x.*P1',mask1);%反量化
I1=blkproc(X1,[8,8],'P1*x*P2',D',D);%重构图像-IDCT
subplot(1,2,1),imshow(I),title('加密')
subplot(1,2,2),imshow(I1),title('JPEG')
% I1=C;
%%