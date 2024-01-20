/*************************************************************************//**
 *****************************************************************************
 * @file   open.c
 * @brief  open()
 * @author Forrest Y. Yu
 * @date   2008
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
 *                                open
 *****************************************************************************/
/**
 * open/create a file.
 * 
 * @param pathname  The full path of the file to be opened/created.
 * @param flags     O_CREAT, O_RDWR, etc.
 * 
 * @return File descriptor if successful, otherwise -1.
 *****************************************************************************/
PUBLIC int open(const char *pathname, int flags)
{
	MESSAGE msg;

	msg.type	= OPEN;

	msg.PATHNAME	= (void*)pathname;
	msg.FLAGS	= flags;
	msg.NAME_LEN	= strlen(pathname);

	send_recv(BOTH, TASK_FS, &msg);
	assert(msg.type == SYSCALL_RET);

	return msg.FD;
}
PUBLIC int test_ls(){
	MESSAGE msg;

        msg.type        = LIST;

        //msg.PATHNAME    = (void*)pathname;
        //msg.FLAGS       = flags;
        //msg.NAME_LEN    = strlen(pathname);
	
        send_recv(BOTH, TASK_FS, &msg);
        assert(msg.type == SYSCALL_RET);
		//printf("------------SSAA%s++++",msg.list_info);
		char *res="";
		memcpy(res,msg.list_info,strlen(msg.list_info));
        return res;


}

char *global = "here is global";
void test_global(){
	printf("%s\n", global);
}
/*int hash(const char *name, int length)
{
  unsigned int v2;
  int i;

  v2 = 1377;
  for ( i = 0; i < length; ++i )
    v2 = name[i] + 17 * v2;
  return v2;
}

*/




