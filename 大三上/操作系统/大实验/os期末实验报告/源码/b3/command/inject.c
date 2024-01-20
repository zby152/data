#include "stdio.h"
#include "string.h"
#include "elf.h"

#define PAGESIZE 4096

void cal_addr(int entry, int addr[]) {
    int temp = entry;
    int i;
    for (i = 0; i < 4; i++) {
        addr[i] = temp % 256;
        temp /= 256;
    }
}

void inject(char* elf_file) {
    printf("start to inject...\n");

    int old_entry;
    Elf32_Ehdr elf_ehdr;
    Elf32_Phdr elf_phdr;

    int old_file = open(elf_file, O_RDWR);
    read(old_file, &elf_ehdr, sizeof(Elf32_Ehdr));
    old_entry = elf_ehdr.e_entry;
    printf("old_entry: %x\n", old_entry);

    // Modify e_shoff of ELF Header，adding PAGESIZE
    // elf_ehdr.e_shoff += PAGESIZE;

    int i = 0;

    printf("Modifying the program header table...\n");
    // 读取并修改程序头部表
    close(old_file);
    old_file = open(elf_file, O_RDWR);
    char buffer[20000];
    read(old_file, buffer, elf_ehdr.e_phoff);
    read(old_file, &elf_phdr, sizeof(elf_phdr));

    printf("Inserting the injector...\n");
    // 插入注入程序
    close(old_file);
    insert(elf_ehdr, elf_file, old_entry);
}

void insert(Elf32_Ehdr elf_ehdr, char* elf_file, int old_entry) {
    // 程序的原始入口地址
    int old_entry_addr[4];
    cal_addr(old_entry, old_entry_addr);

    // printf("old_entry = 0x%x%x%x%x\n", old_entry_addr[3],old_entry_addr[2],old_entry_addr[1],old_entry_addr[0]);
    // 每一行对应一条汇编代码
    char inject_code[] = {
        0x68,
        0x78,
        0x17,
        0x00,
        0x00,
        0xe8,
        0x20,
        0x00,
        0x00,
        0x00,
    };
    int inject_size = sizeof(inject_code);

    // 防止注入代码太大
    if (inject_size > PAGESIZE) {
        printf("Injecting code is too big!\n");
        exit(0);
    }
    int old_file = open(elf_file, O_RDWR);
    u8 buffer[20000];
    read(old_file, buffer, 0x1024);
    write(old_file, inject_code, inject_size);
    close(old_file);
    old_file = open(elf_file, O_RDWR);
    read(old_file, buffer, 0x1024);
    read(old_file, buffer, 10);
    for (int i = 0; i < 10; i++) {
        printf("%x\n", buffer[i]);
    }

    printf("Finished!\n");
}

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("inject <elf_filepath>\n");
        exit(0);
    }
    inject(argv[1]);
    return 0;
}
