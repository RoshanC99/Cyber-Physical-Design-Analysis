#include <pthread.h>
#include <stdlib.h>

#include "periodic_task.h"
#include "utils.h"

typedef struct _task_parameters {
  struct timespec period;	/* period of a task */
  void (*job) (void);		/* parameter-less function, executed at each
				 * dispatch */
}                task_parameters;

/*****************************************************************************/
void *periodic_task_body (void *parameters);

void *periodic_task_body (void *parameters) {
  struct timespec trigger;	/* Stores next dispatch time */
  struct timespec period;	/* Period of the task */

  task_parameters *my_parameters = (task_parameters *) parameters;

  pthread_cond_t cv;
  pthread_mutex_t m;

  CHECK_NZ (pthread_cond_init (&cv, NULL));
  CHECK_NZ (pthread_mutex_init (&m, NULL));

  period = (*my_parameters).period;
  clock_gettime (CLOCK_REALTIME, &trigger);	/* Initialize timer */

  for (;;) {			/* Infinite periodic loop */
    my_parameters->job ();

    add_timespec (&trigger, &trigger, &period);	/* Compute next dispatch time */
    CHECK_NZ (pthread_mutex_lock (&m));
    pthread_cond_timedwait (&cv, &m, &trigger);
    /* Wait until next trigger */
    CHECK_NZ (pthread_mutex_unlock (&m));
  }
}

/*****************************************************************************/
void create_periodic_task (struct timespec period, void (*job) (void)) {
  pthread_t tid;
  task_parameters *parameters = malloc (sizeof (task_parameters));

  parameters->period = period;
  parameters->job = job;

  pthread_create (&tid, NULL, periodic_task_body, (void *)parameters);
}
