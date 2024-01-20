#include "stdio.h"
void vuln(){
	char buf[0x100];
	int fd = open("payload", O_RDWR);
	if(fd < 0) return printf("open file error \n");
	read(fd, buf, 0x200);
	return ;


}
int main(){
	vuln();
	printf("hello world!\n");

}
void backdoor(){
	printf("here is backdoor!\n");
}

