//kernel/clock.c  line 34
//kernel/clock.c  line 59
#include "type.h"
#include "stdio.h"
#include "const.h"
#include "protect.h"
#include "tty.h"
#include "console.h"
#include "string.h"
#include "fs.h"
#include "proc.h"
#include "global.h"
#include "proto.h"

PRIVATE void block(struct proc* p);
PRIVATE void unblock(struct proc* p);
PRIVATE int  msg_send(struct proc* current, int dest, MESSAGE* m);
PRIVATE int  msg_receive(struct proc* current, int src, MESSAGE* m);
PRIVATE int  deadlock(int src, int dest);


int inqueue(struct proc* p)
{
	QUEUE* tempqueue;
	tempqueue=queue+p->queuenum;
	tempqueue->taskqueue[tempqueue->rear]=p;
	tempqueue->rear=(tempqueue->rear+1)%QUEUE_LEN;
	p->inqueue=1;
	tempqueue->len+=1;
}

int outqueue(struct proc* p)
{
	QUEUE* tempqueue;
	tempqueue=queue+p->queuenum;
	tempqueue->front=(tempqueue->front+1)%QUEUE_LEN;
	p->inqueue=0;
	tempqueue->len-=1;
}


struct proc* get_one_proc()
{
	struct	proc* p;
    	QUEUE* tempqueue;
	int now_queue_num = 0;

	for (p = &FIRST_PROC; p <= &LAST_PROC; p++)
	{
		if (p->p_flags == 0 && p->inqueue == 0 &&(p != p_proc_ready || queue->len == 0))
		{
			p->ticks = queue->timep;
			p->queuenum = 0;
			p->runtime = 10;
			inqueue(p);
		}
	}
	now_queue_num = 0;

	while (now_queue_num <= 2)
	{
		tempqueue = queue + now_queue_num;
		int length = 0;
		int point = tempqueue->front;
		while (tempqueue->taskqueue[point]->p_flags != 0 && length < tempqueue->len)
		{
			outqueue(tempqueue->taskqueue[point]);
			inqueue(tempqueue->taskqueue[point]);
			length += 1;
			point = (point + 1) % QUEUE_LEN;
		}
		if (length < tempqueue->len)
		{
			return tempqueue->taskqueue[point];
		}
		now_queue_num++;
	}
}


PUBLIC void myschedule()
{
	struct proc *p,*next;
	next=get_one_proc();
	
	if(p_proc_ready->ticks && p_proc_ready->runtime && next->queuenum >= p_proc_ready->queuenum)
	{
		return;
	}
	
	if(p_proc_ready->runtime ==0)
	{
		p_proc_ready=next;
		outqueue(next);
		return ;
	}
	
	if(p_proc_ready->ticks==0)
	{
		if(p_proc_ready->queuenum<2)
		{
			p_proc_ready->queuenum+=1;
		}
		p_proc_ready->ticks=(queue+p_proc_ready->queuenum)->timep;
		inqueue(p_proc_ready);
		p_proc_ready=next;
		outqueue(next);
		return;
	}
	if(next->queuenum < p_proc_ready->queuenum)
	{
		inqueue(p_proc_ready);
		p_proc_ready=next;
		outqueue(next);
		return;
	}
}
