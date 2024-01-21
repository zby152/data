#include <iostream>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
using namespace std;

//关键字 
string key[3]={"assign","if","else"};    
//关键字的种别码
int key_class[3]={1,2,3}; 

//运算符和界符 
string symbol[17]={"<",">","!=",">=","<=","==",",",";","(",")","{","}","+","-","*","/","="};
//运算符和界符的种别码 
int symbol_class[17]={4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};

string letter[1000];//存放文件取出的字符


string  words[1000];//存放单词
int length;  //程序中字符的数目 
int num; //当前扫描到的位置

string number_table[1000];//常数表
int word_i;
string word_table[1000];//标识符表
int number_i;

//判断运算符和界符
int is_symbol(string s) 
{ 
	int i;
    for(i=0;i<17;i++)
	{
        if(s==symbol[i])
            return symbol_class[i]; 
    }
    return 0;
} 

//判断是否为数字 
bool is_number(string s)
{
	if(s>="0" && s<="9")
        return true;
    return false;
}

//判断是否为字母 
bool is_letter(string s)
{
    if(s>="a" && s<="z")
        return true;
    return false;
}

//判断是否为关键字,是返回种别码 
int is_keyword(string s)
{
	int i;
	for(i=0;i<6;i++)
    {
		if(s==key[i])
			return key_class[i];
	}
	return 0;
}
 
//返回单个字符的类型 
int type_word(string str)
{
	if(str>="a" && str<="z")   //	字母 
        return 1;   
    else if(str>="0" && str<="9")   //数字 
        return 2; 
    else if(str==">"||str=="="||str=="<"||str=="!"||str==","||str==";"||str=="("||str==")"||str=="{"||str=="}"
		||str=="+"||str=="-"||str=="*"||str=="/")   //判断运算符和界符 
        return 3; 
	else if(str=="#")
		return 4;
	else
		return 5;
}

//标识符的连接
string letter_connecter(string s,int n)
{
	int j=n+1;
	int flag=1;
	
	while(flag)
    {
		if(is_number(letter[j]) || is_letter(letter[j]))
        {
			s=(s+letter[j]).c_str();
			if(is_keyword(s))
            {
				j++;
				num=j;
				return s;
			}
			j++;
		}
		else
        {
			flag=0;
		}
	} 
	
	num=j;
	return s;
}

//符号和界符的链接
string symbol_connecter(string s,int n)
{
	int j=n+1;
	string str=letter[j];
	if(str==">"||str=="="||str=="<"||str=="!") 
    {
		s=(s+letter[j]).c_str();
		j++;
	}
	num=j;
	return s;
}

//链接数字函数
string number_connecter(string s,int n)
{
	int j=n+1;
	int flag=1;
	
	while(flag)
    {
		if(is_number(letter[j]))
        {
			s=(s+letter[j]).c_str();
			j++;
		}
		else 
			flag=0;
	}
	num=j;
	return s;
}

//输出函数
void print(string s,int n,int m)
{
	cout<<"("<<s<<","<<n<<","<<m<<")"<<endl;
}

void take_word()//取字符
{   
    int k;
	while(1)
	{
		string str1,str;
		str=letter[num];
		k=type_word(str);
		switch(k)
		{
			case 1:
			{
				str1=letter_connecter(str,num);
				if(is_keyword(str1))
					print(str1,is_keyword(str1),0);
				else
                {
                    int find = 0;
                    for (int i = 1; i <= word_i;i++)
                    {
                        if(word_table[i]==str1)
                        {
                            print(str1, 21, i);
                            find = 1;
                        }
                    }
                    if(!find)
                    {
                        word_i++;
                        word_table[word_i] = str1;
                        print(str1,21,word_i);
                    }
                }
				break;
			}
			
		    case 2:
		    {
		    	str1=number_connecter(str,num);
				int find = 0;
				for (int j = 1; j <= number_i;j++)
				{
					if(number_table[j]==str1)
					{
						print(str1, 22, j);
					    find = 1;
					}
				}
				if(!find)
				{
                     number_i++;
                    number_table[number_i] = str1;
                    print(str1,22,number_i);
				}
				break;
			}

		    case 3:
		    {
			    str1=symbol_connecter(str,num);
			    print(str1,is_symbol(str1),0);
			    break;	
			}

			case 4:
			{
				return;
			}
		    
			default:
			{
                cout<<"ERROR"<<endl;
				return;
			}
		}
		
	} 
}

int main()
{
	char w;
	int i,j;

	freopen("program.txt","r",stdin);
	freopen("result.txt","w",stdout);

	cout << "(word,class,value)" << endl;
	length=0;

	while(cin>>w) //将字符载入letter数组中
    {
		if(w!=' ')
        {
			letter[length]=w;
			length++;
		}   
	}
	
	take_word();

	fclose(stdin);//关闭文件 
    fclose(stdout);//关闭文件

	freopen("number_table.txt", "w", stdout);//输出数字表
	cout << "(number,pointer)" << endl;
	for (int i = 1; i <= number_i;i++)
	{
		cout << "(" << number_table[i] << "," << i << ")" << endl;
	}
	fclose(stdout);

    freopen("word_table.txt", "w", stdout);//输出标识符表
	cout << "(word,pointer)" << endl;
	for (int i = 1; i <= word_i;i++)
	{
		cout << "(" << word_table[i] << "," << i << ")" << endl;
	}
	fclose(stdout);

	return 0;
} 
