/*
 * periodic_task.h: a factory of periodic task
 */

#ifndef __PERIODIC_TASK_H__
#define __PERIODIC_TASK_H__

#include <pthread.h>
#include <time.h>

void create_periodic_task (struct timespec period, void (*job) (void));
/*
 * Create a periodic task, of period 'period'. At each dispatch, it will
 * execute the job function
 */

#endif				/* __PERIODIC_TASK_H__ */
