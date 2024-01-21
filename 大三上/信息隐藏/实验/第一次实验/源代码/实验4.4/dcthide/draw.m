A=[0.1,0.01,0.001,0.0005,0.0004,0.0001,0.00001];
[x,len]=size(A);
result=zeros(1, len);
for i=1:len
    result(i)=dcthide2(A(i));
end
resultt=result./504;
