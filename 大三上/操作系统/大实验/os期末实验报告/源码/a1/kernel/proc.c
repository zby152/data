
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                               proc.c
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                                                    Forrest Yu, 2005
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#include "type.h"
#include "const.h"
#include "protect.h"
#include "proto.h"
#include "string.h"
#include "proc.h"
#include "global.h"

PRIVATE void delete_proc() {
	int queue = p_proc_ready->queue;
	if (queue == 1) {
		first_num--;
	} else if (queue == 2) {
		second_num--;
	} else { // if (queue == 3)
		third_num--;
	}
	p_proc_ready->queue = 0;

	PROCESS* p;
	for (p = proc_table; p < proc_table + NR_TASKS; p++) {
		if (p->queue == queue) p->pos--;
	}
}

PRIVATE void add_proc() {
	p_proc_ready->ticks = p_proc_ready->priority;
	p_proc_ready->ft = first_ticks;
	p_proc_ready->st = second_ticks;
	p_proc_ready->tt = third_ticks;
	p_proc_ready->queue = 1;
	p_proc_ready->pos = first_num;
	first_num++;
}

PUBLIC void disp_queue() {
	if (finish_proc_num == 7) return;
    disp_str("1:");
	for (int i = 0; i < first_num; i++) {
		PROCESS* p;
		for (p = proc_table; p < proc_table + NR_TASKS; p++) {
			if (p->pos == i && p->queue == 1) {
				disp_str(p->p_name);
                disp_str("<");
                disp_int(p->ticks);
                disp_str(">");
				disp_str(" ");
			}
		}
	}

	disp_str("|2:");
	for (int i = 0; i < second_num; i++) {
		PROCESS* p;
		for (p = proc_table; p < proc_table + NR_TASKS; p++) {
			if (p->pos == i && p->queue == 2) {
				disp_str(p->p_name);
                disp_str("<");
                disp_int(p->ticks);
                disp_str(">");
				disp_str(" ");
			}
		}
	}

	disp_str("|3:");
	for (int i = 0; i < third_num; i++) {
		PROCESS* p;
		for (p = proc_table; p < proc_table + NR_TASKS; p++) {
			if (p->pos == i && p->queue == 3) {
				disp_str(p->p_name);
                disp_str("<");
                disp_int(p->ticks);
                disp_str(">");
				disp_str(" ");
			}
		}
	}
	disp_str("\n");

	dbg_disp_time++;
	if (dbg_disp_time == 25) {
		// return;
        disp_pos = 0;
        for (int i = 0; i < 80 * 25; i++) {
            disp_str(" ");
        }
        disp_pos = 0;
        dbg_disp_time++;
    }
}

/*======================================================================*
                              schedule
 *======================================================================*/
PUBLIC void schedule()
{
	if (p_proc_ready->ticks == 0) {
		delete_proc();
		p_proc_ready->out_ticks = get_ticks();
		finish_proc_num++;
		if (finish_proc_num == NR_TASKS) {
			disp_str(" PROC_NAME |  submit  |  finish   | response |  waiting  |\n");
			int i = 1;
			for (PROCESS* p = proc_table; p < proc_table + NR_TASKS; p++) {
				disp_str("PROCESS ");
				disp_int(i);
				i++;
				disp_str("|    ");
				disp_int(p->in_ticks);
				disp_str("   |   ");
				disp_int(p->out_ticks);
				disp_str("   |   ");
				disp_int(p->resp_ticks);
				if (i == 2) disp_str(" ");
				disp_str("   |   ");
				disp_int(p->out_ticks - p->priority);
				disp_str("   |\n");
			}
		}
		// add_proc();
	} else if (p_proc_ready->queue == 1) {
		delete_proc();
		p_proc_ready->queue = 2;
		p_proc_ready->pos = second_num;
		second_num++;
	} else if (p_proc_ready->queue == 2) {
		delete_proc();
		p_proc_ready->queue = 3;
		p_proc_ready->pos = third_num;
		third_num++;
	} else { // if (p_proc_ready->queue == 3)
		delete_proc();
		p_proc_ready->queue = 3;
		p_proc_ready->pos = third_num;
		third_num++;
		p_proc_ready->tt = third_ticks;
	}

    if (finish_proc_num < NR_TASKS) {
		disp_queue();
    }

	// find next
	PROCESS* p;
	for (p = proc_table; p < proc_table + NR_TASKS; p++) {
		if (p->pos == 0 && p->queue == 1) {
			p_proc_ready = p;
			return;
		}
	}

	for (p = proc_table; p < proc_table + NR_TASKS; p++) {
		if (p->pos == 0 && p->queue == 2) {
			p_proc_ready = p;
			return;
		}
	}

	for (p = proc_table; p < proc_table + NR_TASKS; p++) {
		if (p->pos == 0 && p->queue == 3) {
			p_proc_ready = p;
			return;
		}
	}
}

/*======================================================================*
                           sys_get_ticks
 *======================================================================*/
PUBLIC int sys_get_ticks()
{
	return ticks;
}

