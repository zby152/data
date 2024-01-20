
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                               clock.c
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


/*======================================================================*
                           clock_handler
 *======================================================================*/
PUBLIC void clock_handler(int irq)
{
    if (p_proc_ready->resp_ticks == -1) p_proc_ready->resp_ticks = ticks;
	ticks++;

	if (k_reenter != 0) {
		return;
	}

	if (p_proc_ready->ft > 0 && p_proc_ready->queue == 1) {
		if (p_proc_ready->ticks > 0) {
			p_proc_ready->ft--;
			p_proc_ready->ticks--;
			return;
		}
	}

	if (p_proc_ready->st > 0 && p_proc_ready->queue == 2) {
		if (p_proc_ready->ticks > 0) {
			p_proc_ready->st--;
			p_proc_ready->ticks--;
			return;
		}
	}

	if (p_proc_ready->tt > 0 && p_proc_ready->queue == 3) {
		if (p_proc_ready->ticks > 0) {
			p_proc_ready->tt--;
			p_proc_ready->ticks--;
			return;
		}
	}

	schedule();
}

/*======================================================================*
                              milli_delay
 *======================================================================*/
PUBLIC void milli_delay(int milli_sec)
{
        int t = get_ticks();

        while(((get_ticks() - t) * 1000 / HZ) < milli_sec) {}
}

