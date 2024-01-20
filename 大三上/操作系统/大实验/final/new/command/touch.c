# include "stdio.h"

int main(int args,char* argv[])
{
	int fd=open(argv[1],O_CREAT);
	if(fd!=-1)
	{
		printf("creat %s successfully\n",argv[1]);
	}
	else
	{
		printf("faile to creat %s\n",argv[1]);
	}
	
	return 0;
}
