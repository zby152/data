#include <linux/init.h>
#include <linux/init_task.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/sched.h>
#include <linux/types.h>

#define MAXN 256

MODULE_LICENSE("GPL");

struct stack
{
    struct task_struct *data[MAXN];
    int head;
} st; // 定义堆栈结构变量

int st_size(void)
{
    return st.head;
}

bool st_empty(void)
{
    return st.head == 0;
}
bool st_full(void)
{
    return st.head == MAXN;
}

struct task_struct *st_pop(void) // 定义出栈函数
{
    if (st_empty())
        return NULL;
    st.head -= 1;
    return st.data[st.head];
}
bool st_push(struct task_struct *t) // 定义入栈函数
{
    if (st_full())
        return false;
    st.data[st.head++] = t;
    return true;
}

static int my_module_init(void) // 加载模块函数
{

    st.head = 0;
    st_push(&init_task);

    struct task_struct *tsk, *p;
    struct list_head *list, *list2;
    while (!st_empty()) // 当每次栈不空时进行循环
    {
        tsk = st_pop();
        if ((&tsk->children)->next != (&tsk->children))
            printk(KERN_INFO "The child processes of %s (with pid:%d) is:\n", tsk->comm, tsk->pid);
        list_for_each_prev(list, &tsk->children)
        {
            p = list_entry(list, struct task_struct, sibling);
            st_push(p);
        }
        list_for_each(list2, &tsk->children)
        {
            p = list_entry(list2, struct task_struct, sibling);
            printk(KERN_INFO "name [%s] status [%d] pid [%d]\n", p->comm, p->stats, p->pid); // 输出进程的名称，状态以及进程号
        }
    }
    return 0;
}

static void __exit my_module_exit(void) // 进程的卸载函数
{
    printk(KERN_INFO "Exiting my_module.\n");
}

module_init(my_module_init);
module_exit(my_module_exit);