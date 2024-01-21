#include <linux/init.h>
#include <linux/init_task.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/sched.h>

MODULE_LICENSE("GPL");

static int __init my_module_init(void)//模块的加载
{
    struct task_struct *p;
    p = NULL;
    p = &init_task;
    printk(KERN_INFO "ListTask module loaded\n");
    printk(KERN_INFO "PID\tStatus                    Name\n");//列出表头方便显示
    for_each_process(p)
    {
        printk(KERN_INFO "%d\t%ld\t%s\n", p->pid, p->stats, p->comm);//依次列出每一个进程的进程号，状态以及进程名称
    }

    return 0;
}

static void __exit my_module_exit(void)//模块的卸载
{
    printk(KERN_INFO "Exiting my_module.\n");
}

module_init(my_module_init);
module_exit(my_module_exit);
