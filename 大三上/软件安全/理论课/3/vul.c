#include <stdio.h>
#include<string.h>

void main(int argc, char ** argv)
{
   static int a=0;
   int b=0;
   char buff[200];
   char ch;
   printf("the addresses of a b buf are %p,%p,%p\n", &a, &b, buff);
   
   strcpy(buff,argv[1]);
   printf(buff);
   printf("\n");
   printf("a= %d\n", a);
   return 0;
}
   

