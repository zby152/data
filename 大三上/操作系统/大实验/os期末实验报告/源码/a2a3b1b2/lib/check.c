#include "stdio.h"
#include "elf.h"
#include "type.h"
#include "const.h"
#include "protect.h"
#include "string.h"
#include "fs.h"
#include "proc.h"
#include "tty.h"
#include "console.h"
#include "global.h"
#include "proto.h"

PUBLIC u32 check(char* filename, int byteCount) {
    int hFile = open(filename, O_RDWR);
    if (hFile < 0) {
        return -1;
    }

    u8 plaintext[16] = {0};
    u8 ciphertext[16] = {0};
    u32 key[4] = {0x12345678, 0x20193021, 0x40023201, 0x93021400};
    u32 current_checkSum = 0;

    // FINISHED: 一块一块读，加快check速度
    u8 buffer[byteCount];
    read(hFile, buffer, byteCount);
    for (int i = 0; i < byteCount; i++) {
        plaintext[i % 16] = buffer[i];
        if ((i % 16 == 0 && i != 0) || (i == byteCount - 1)) {
            aes_enc(ciphertext, plaintext, key);
            for (int j = 0; j < 4; j++) {
                u32 temp = ((u32)ciphertext[4 * j + 0] << 24) |
                           ((u32)ciphertext[4 * j + 1] << 16) |
                           ((u32)ciphertext[4 * j + 2] <<  8) |
                           ((u32)ciphertext[4 * j + 3] <<  0);
                current_checkSum ^= temp;
            }
        }
    }
    close(hFile);
    return current_checkSum;
}

PUBLIC int find_position(struct check_t check_table[], char* filename) {
    for (int i = 0; i < NR_CHECKFILES; i++) {
        int flag = strcmp((check_table + i)->filename, filename);
        if (flag == 0) {
            return i;
        }
    }
    return -1;
}
