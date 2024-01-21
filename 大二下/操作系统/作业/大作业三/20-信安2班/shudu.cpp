#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>


void *column_checker(void *param);   
void *row_checker(void *param);     
void *block_checker(void *param); 


//示例数独
int example[9][9] = {
    { 6, 2, 4, 5, 3, 9, 1, 8, 7},
    { 5, 1, 9, 7, 2, 8, 6, 3, 4},
    { 8, 3, 7, 6, 1, 4, 2, 9, 5},
    { 1, 4, 3, 8, 6, 5, 7, 2, 9},
    { 9, 5, 8, 2, 4, 7, 3, 6, 1},
    { 7, 6, 2, 3, 9, 1, 4, 5, 8},
    { 3, 7, 1, 9, 5, 6, 8, 4, 2},
    { 4, 9, 6, 1, 8, 2, 3, 3, 3},
    { 2, 8, 5, 4, 7, 3, 9, 1, 3}};

//判断数独是否有效数组，初始值为零，每个线程控制一位，为零则对应的线程区域无效
int judge[11] = {1,1,1,1,1,1,1,1,1,1,1};

typedef struct
{
    int row;
    int column;
} parameters;

int main(int argc, char *argv[])
{
    parameters *data = (parameters *)malloc(sizeof(parameters));
    data->row = 1;
    data->column = 1;

    //创建线程id
    pthread_t tid_row;
    pthread_t tid_column;
    pthread_t tid_subfield;

    //创建线程
    pthread_create(&tid_row, NULL, row_checker, (void *)data);
    pthread_create(&tid_column, NULL, column_checker, (void *)data);
    pthread_create(&tid_subfield, NULL, block_checker, (void *)data);

    //线程阻塞
    pthread_join(tid_row, NULL);
    pthread_join(tid_column, NULL);
    pthread_join(tid_subfield, NULL);

    printf("本次测试的数独为:\n");
    for (int i = 0; i < 9;i++)
    {
        for (int j = 0; j < 9;j++)
        {
            printf("%d ", example[i][j]);
        }
        printf("\n");
    }
    
    int result = 1;       //有效与否的总结果

    //对数组中的每个值求乘积不为零则所有检查均有效
    for (int k = 0; k <= 10;k++)
    {
        //printf("%d", judge[k]);
        result *= judge[k];
    }

    if (result == 1)
    {
        printf("数独猜谜有效\n");
    }
    else
    {
        printf("数独猜谜无效\n");
    }

    return 0;
}

//列检查函数
void *row_checker(void *params)
{

    parameters *temp_row;
    temp_row = (parameters *)params;

    for (int i = temp_row->row; i <= 9; i++)
    {
        int flag[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0,0};  //每检查一个数字就在flag数组对应位置填入1，若重复填写则该区域发生错误
        for (int j = temp_row->column; j <= 9; j++)
        {
            if (flag[example[i-1][j-1]] == 0)  //检查正确
            {
                flag[example[i-1][j-1]] = 1;
            }
            else if (flag[example[i-1][j-1]] == 1)//出现错误
            {
                printf("第%d行不满足\n", i);//输出发生错误对应的部分
                judge[0]=0;
                break;
            }
        }
    }
    pthread_exit(0);
}

//行检查函数
void *column_checker(void *params)
{
    parameters *temp;
    temp = (parameters *)params;
    for (int i = temp->column; i <= 9; i++)
    {
        int flag[10] = {0,0, 0, 0, 0, 0, 0, 0, 0, 0};    //每检查一个数字就在flag数组对应位置填入1，若重复填写则该区域发生错误
        for (int j = temp->row; j <= 9; j++)
        {
            if (flag[example[j-1][i-1]] == 0)//检查正确
            {
                flag[example[j-1][i-1]] = 1;
            }
            else if (flag[example[i-1][j-1]] == 1)//出现错误
            {
                printf("第%d列不满足\n", i);//输出发生错误对应的部分
                judge[1]=0;
                break;
            }
        }
    }
    pthread_exit(0);
}

//块检查函数
void *block_checker(void *params)
{
    parameters *temp;
    temp = (parameters *)params;

    int block = 1;    //当前正在检查的块编号

    for (int i = temp->row; i <= 9; i += 3)
    {
        for (int j = temp->column; j <= 9; j += 3)  //确定要检查哪一块
        {
            int exit = 0;
            int flag[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};//每检查一个数字就在flag数组对应位置填入1，若重复填写则该区域发生错误
            for (int a = 0; a < 3; a++)
            {
                for (int b = 0; b < 3; b++)  //确定检查该块的哪一个位置
                {
                    if (flag[example[i + a-1][j + b-1]] == 0)//检查正确
                    {
                        flag[example[i + a-1][j + b-1]] = 1;
                    }
                    else if (flag[example[i + a-1][j + b-1]] == 1)//检查错误
                    {
                        judge[block+1]=0;
                        printf("第%d块不满足\n", block);//输出发生错误的部位
                         exit = 1;
                        break ;
                    }
                }
                if(exit==1)
                {
                    break;
                }
            }
            block++;
        }
    }
    pthread_exit(0);
}
