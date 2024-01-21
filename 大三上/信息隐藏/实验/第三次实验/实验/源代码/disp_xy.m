%绘制SC图
function disp_xy(x,y,y_DCT,top_title,x_label,type)
if(type==0)
    figure;
    x_max=max(x);
    x_inc=x(2)-x(1);
    plot(x,y,'-*b',x,y_DCT,'-or'); 
    axis([0,x_max,0,1])  
    set(gca,'XTick',[0:x_inc:x_max]) 
    set(gca,'YTick',[0:0.1:1]) 
    legend('相关系数','DCT相关系数');
    title(top_title)
    xlabel(x_label)  
    ylabel('相关性') 
elseif(type==1)
    figure;
    X=1:7;
    plot(X,y,'-*b',X,y_DCT,'-or'); 
    xlim([0 7])  
    set(gca,'xtick',1:7) 
    set(gca,'xticklabel',x)
    xtickangle(45);
    set(gca,'YTick',[0:0.1:1]) 
    legend('相关系数','DCT相关系数');
    title(top_title)
    xlabel(x_label)  
    ylabel('相关性') 
end