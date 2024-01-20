#include <stdio.h>
int i;
int* addr;

void test() {
    printf("pya, whx, thm, pzx\n");
}

void testat() {
    char buff[72] = {0};
    for (i = 0; i < 72; i++) {
        buff[i] = 0;
    }

    for (; i < 72; i++) {
        buff[i] = 0;
    }

    addr = &buff[72];
    for (i = 0; i < 3; i++) {
        addr[i] = 0x1000;
    }
}

void main(int argc, char* argv[]) {
    testat();
}