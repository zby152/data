# include "stdio.h"
# include "string.h"

void main(int argc, char * argv[])
{
	char buff[200] = {0};
	int a = 0;
	int b = 0;

	char ch;

	printf("the addresses of a b buf are %x,%x,%x\n", &a, &b, buff);
	strcpy(buff,argv[1]);

	a = 0;
	printf(buff);
	printf("\n");
	printf("a= %d\n", a);
	return 0;
}
