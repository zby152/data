#include<stdio.h>
#include<string.h>
#include<pthread.h>
#include<unistd.h>
#include<semaphore.h>

sem_t ta,student;   //无名信号量ta和student
pthread_mutex_t mutex;  //互斥锁数据类型
int waiting = 0;  //等待的学生数


void* teaching(void *value)
{
	while(true)
    {
		sem_wait(&student);  //获得信号量
		pthread_mutex_lock(&mutex);  //获取互斥锁
		waiting--;
		pthread_mutex_unlock(&mutex);  //释放互斥锁
		printf("TA is teaching\n");
		sleep(5);
		sem_post(&ta);   //释放信号量
		printf("TA is sleeping\n");
	}
}
void* consulting(void *value)
{
	while(true)
    {
		pthread_mutex_lock(&mutex);
		if(waiting<=3)//有椅子，可以等待
        {
			waiting++;
			pthread_mutex_unlock(&mutex);
			printf("student%lu is waiting for TA\n",pthread_self());
			sem_post(&student);
			sem_wait(&ta);
			printf("student%lu is consulting the TA\n",pthread_self());
			sleep(5);
			printf("consultiation is over\n");
		}
		else//没有椅子
        {
			pthread_mutex_unlock(&mutex);
			printf("No more chairs,student%lu has left\n",pthread_self());
			sleep(3);
		}
	}
}

int main()
{
	pthread_t student1,student2,student3,student4,student5,teacher;

    //初始化无名信号量
	sem_init(&ta,0,1);  
	sem_init(&student,0,0);

	//创建互斥锁
	pthread_mutex_init(&mutex,NULL);

    //创建线程
	pthread_create(&student1,NULL,consulting,NULL);//学生线程
	pthread_create(&student2,NULL,consulting,NULL);
	pthread_create(&student3,NULL,consulting,NULL);
	pthread_create(&student4,NULL,consulting,NULL);
	pthread_create(&student5,NULL,consulting,NULL);
	pthread_create(&teacher,NULL,teaching,NULL);//TA助教线程
	
	//线程间的阻塞
	pthread_join(student1,NULL);//学生线程
	pthread_join(student2,NULL);
	pthread_join(student3,NULL);
	pthread_join(student4,NULL);
	pthread_join(student5,NULL);
	pthread_join(teacher,NULL);//TA助教线程
	
	return 0;
}
