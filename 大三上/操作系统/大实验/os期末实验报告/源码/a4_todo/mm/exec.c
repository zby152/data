/*************************************************************************//**
 *****************************************************************************
 * @file   mm/exec.c
 * @brief  
 * @author Forrest Y. Yu
 * @date   Tue May  6 14:14:02 2008
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
#include "keyboard.h"
#include "proto.h"
#include "elf.h"

#define PG_PAGE_OFFSET 12

/*
 * size为分配的页数
 * addr为起始地址---物理地址
 * 假设为页对齐,且不会重复分配同一段内存
 */
Elf32_Addr addMapping(int src, ptr_pt p, Elf32_Addr addr, int size) {
    assert(size <= 1024);
    assert(((addr & PG_DIR_MASK) >> PG_DIR_OFFSET) == 3);
    if (p->pde_alloc[(addr & PG_DIR_MASK) >> PG_DIR_OFFSET] == 0) {
        // 该pde未分配页表项,分配一个新的页表项
        p->alloc_size++;
        assert(p->alloc_size <= 15);
        p->pde_alloc[(addr & PG_DIR_MASK) >> PG_DIR_OFFSET] = p->alloc_size;
        p->pde[(addr & PG_DIR_MASK) >> PG_DIR_OFFSET] = (u32)_va2la(src, (void*)(p->alloc_size * PT_SIZE_DEFAULT)) | PG_P | PG_USU | PG_RWW;
    }
    int idx = p->pde_alloc[(addr & PG_DIR_MASK) >> PG_DIR_OFFSET] - 1;
    Elf32_Addr ret = p->alloc_addr;
    int pte_start = (addr & PG_PAGE_MASK) >> PG_PAGE_OFFSET;
    for (int i = 0; i < size; i++) {
        p->pte[i + idx * 1024 + pte_start] = (u32)_va2la(src, (void*)p->alloc_addr) | PG_P | PG_USU | PG_RWW;
        p->alloc_addr += 4096;
        assert(p->alloc_addr < PROC_IMAGE_SIZE_DEFAULT - PROC_STACK_SIZE_DEFAULT);
    }
    return ret;
};

/*****************************************************************************
 *                                do_exec
 *****************************************************************************/
/**
 * Perform the exec() system call.
 * 
 * @return  Zero if successful, otherwise -1.
 *****************************************************************************/
PUBLIC int do_exec()
{
	/* get parameters from the message */
	int name_len = mm_msg.NAME_LEN;	/* length of filename */
	int src = mm_msg.source;	/* caller proc nr. */
	assert(name_len < MAX_PATH);

	char pathname[MAX_PATH];
	phys_copy((void*)va2la(TASK_MM, pathname),
		  (void*)va2la(src, mm_msg.PATHNAME),
		  name_len);
	pathname[name_len] = 0;	/* terminate the string */

	/* get the file size */
	struct stat s;
	int ret = stat(pathname, &s);
	if (ret != 0) {
		printl("{MM} MM::do_exec()::stat() returns error. %s", pathname);
		return -1;
	}

	/* read the file */
	int fd = open(pathname, O_RDWR);
	if (fd == -1)
		return -1;
	assert(s.st_size < MMBUF_SIZE);
	read(fd, mmbuf, s.st_size);
	close(fd);

	/* overwrite the current proc image with the new one */
	Elf32_Ehdr* elf_hdr = (Elf32_Ehdr*)(mmbuf);
	int i;
	for (i = 0; i < elf_hdr->e_phnum; i++) {
		Elf32_Phdr* prog_hdr = (Elf32_Phdr*)(mmbuf + elf_hdr->e_phoff +
			 			(i * elf_hdr->e_phentsize));
		if (prog_hdr->p_type == PT_LOAD) {
            // assert(prog_hdr->p_vaddr + prog_hdr->p_memsz <
            //	PROC_IMAGE_SIZE_DEFAULT);
            // phys_copy((void*)va2la(src, (void*)prog_hdr->p_vaddr),
            //	  (void*)va2la(TASK_MM,
            //			 mmbuf + prog_hdr->p_offset),
            //	  prog_hdr->p_filesz);
            int size = ((prog_hdr->p_vaddr + prog_hdr->p_memsz - 1) >> PG_PAGE_OFFSET) - (prog_hdr->p_vaddr >> PG_PAGE_OFFSET) + 1;
            Elf32_Addr alloc_addr = addMapping(src, p, (Elf32_Addr)va2la(src, (void*)prog_hdr->p_vaddr), size);
            phys_copy((void*)va2la(src, (void*)(alloc_addr | (prog_hdr->p_vaddr & PG_PAGE_OFFSET))),
                      (void*)va2la(TASK_MM, mmbuf + prog_hdr->p_offset),
                      prog_hdr->p_filesz);
        }
	}

	/* setup the arg stack */
	int orig_stack_len = mm_msg.BUF_LEN;
	char stackcopy[PROC_ORIGIN_STACK];
	phys_copy((void*)va2la(TASK_MM, stackcopy),
		  (void*)va2la(src, mm_msg.BUF),
		  orig_stack_len);

    Elf32_Addr stack_addr = addMapping(src, p, (Elf32_Addr)va2la(src, (void*)(PROC_IMAGE_SIZE_DEFAULT - PROC_STACK_SIZE_DEFAULT)), 16);
    u8* orig_stack = (u8*)(stack_addr + PROC_STACK_SIZE_DEFAULT - PROC_ORIGIN_STACK);

    int delta = PROC_IMAGE_SIZE_DEFAULT - PROC_ORIGIN_STACK - (int)mm_msg.BUF;

    int argc = 0;
	if (orig_stack_len) {	/* has args */
		char **q = (char**)stackcopy;
		for (; *q != 0; q++,argc++)
			*q += delta;
	}

	phys_copy((void*)va2la(src, orig_stack),
		  (void*)va2la(TASK_MM, stackcopy),
		  orig_stack_len);

	proc_table[src].regs.ecx = argc; /* argc */
    proc_table[src].regs.eax = (u32)PROC_IMAGE_SIZE_DEFAULT - PROC_ORIGIN_STACK;

    /* setup eip & esp */
	proc_table[src].regs.eip = elf_hdr->e_entry; /* @see _start.asm */
    proc_table[src].regs.esp = PROC_IMAGE_SIZE_DEFAULT - PROC_ORIGIN_STACK;

    proc_table[src].regs.pde = (u32)va2la(src, 0);
    phys_copy((void*)va2la(src, 0),
              (void*)va2la(TASK_MM, p),
              PROC_SIZE_PT);

    strcpy(proc_table[src].name, pathname);

	return 0;
}
