%comimage = dctcom('Lena.bmp','bmp')
function comimage = dctcom( image, permission)
f = imread (image, permission) ;
f = double( f) /255;
T = dctmtx( 8) ;
B = blkproc( f, [ 8 8 ] , 'P1*x*P2', T, T') ;

%删除每块中的高频部分
mask = [1 1 1 1 0 0 0 0
        1 1 1 0 0 0 0 0
        1 1 0 0 0 0 0 0
        1 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 ];

B2 = blkproc( B, [8 8] , 'P1.*x', mask) ; 
I2 = blkproc( B2, [8 8] , 'P1*x*P2', T', T) ; 

subplot(121) , imshow(f) ; title( '原始图像') ;
subplot(122) , imshow(I2) ; title( '逆DCT变换后的图像') ;