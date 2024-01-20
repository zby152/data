/*************************************************************************//**
 *****************************************************************************
 * @file   lseek.c
 * @brief  lseek()
 * @author Yuang Peng
 * @date   2021
 *****************************************************************************
 *****************************************************************************/

#include "type.h"
#include "stdio.h"
#include "const.h"
#include "protect.h"
#include "string.h"
#include "fs.h"
#include "proc.h"
#include "tty.h"
#include "console.h"
#include "global.h"
#include "proto.h"

/*****************************************************************************
 *                                lseek
 *****************************************************************************/
/**
 * lseek from a file descriptor.
 *
 * @param fd      File descriptor.
 * @param whence  Mode: SEEK_SET, SEEK_CUR, SEEK_END
 * @param offset  SEEK_SET: The new offset in bytes from the beginning of the file
 *				  SEEK_CUR: The new offset in bytes from (the beginning of the file + offset)
 *				  SEEK_END: The new offset in bytes from (the end of the file + offset)
 *
 * @return
 *****************************************************************************/
PUBLIC int lseek(int fd, int offset, int whence) {
    MESSAGE msg;
	msg.type = LSEEK;
	msg.FD   = fd;
    msg.OFFSET = offset;
    msg.WHENCE = whence;

    send_recv(BOTH, TASK_FS, &msg);

	return msg.CNT;
}
