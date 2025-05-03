/******************************************************************************/
/* FFT Demo
 *
 * This demo illustrates a basic implementaiton of a FFT (Fast Fourier
 * Transform) system.
 *
 * It is made of a periodic task that is sampling a periodic signal,
 * implemented in tAcquireSample() function; and another task that is
 * sampling its value, implemented in tProcessing() function.
 *
 * Both tasks communicate through a message box.
 *
 */
/******************************************************************************/
#define _POSIX_C_SOURCE 199309L // added this to fix CLOCK_REALTIME issue on my WSL2 Ubuntu 22.04
#include <time.h>               // added this to fix CLOCK_REALTIME issue on my WSL2 Ubuntu 22.04             // to compile: do 'make clean && make' and then './fft'

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "complex.h"
#include "list.h"
#include "periodic_task.h"
#include "msg_box.h"
#include "utils.h"

#define ACQUIRE_PERIOD 250    /* Period of the tAcquireSample task, in ms   */
#define PROCESSING_PERIOD 250 /* Period of the tProcessing task, in ms      */

msg_box mbox;
list SignalEntree;
double Time;
double pre_Time;

/******************************************************************************/
/*
 * tAcquireSample: dummy acquisition task this function generates a basic
 * sinusoidal signal.
 */

void tAcquireSample()
{
  double arc1, arc2;
  float Sample;
  const double FirstHarmonicFrequency = 1 / (ACQUIRE_PERIOD * N / 1000.0);
  struct timespec current_time;

  /*
   * Time can be updated eithe knowing the period of activation of the task
   * executing tAcquireSample function, *but* ..
   */

  Time += ACQUIRE_PERIOD / 1000.0;

  /*
   * an important hypothesis is that the actual time of dispatch (awakening
   * of the task) is consistant with this value; or one may use the
   * actual time, computed using the clock_gettime() function
   */

  clock_gettime(CLOCK_REALTIME, &current_time);

  /* Uncomment the line below to use real-time clock */
  Time = current_time.tv_sec + ((double)current_time.tv_nsec) / 1000000000.0;

  /* We generate a sinusoidal signal based on the current value of Time */

  arc1 = 2 * M_PI * FirstHarmonicFrequency * Time;
  arc2 = 2 * M_PI * FirstHarmonicFrequency * 40 * Time;

  Sample = (float)((2.0 * sin(arc1)) + (0.5 * sin(arc2)) + 4.0);

  msg_box_send(mbox, (char *)&Sample);
}

/******************************************************************************/
/*Question 9: UART transmission task*/
void tUARTTransmit()
{
  // wait for new FFT results to be available

  for (int i = 0; i < N; i++) // for each data point
  {
    // UART register writes would go here instead of the printf
    // Wait until UART is ready to transmit
    // then Send the data
  }
}

/******************************************************************************/
/* Processing task                                                            */

static int sample_counter = 0; // Question 8: add sample counter to track when there is full window

void tProcessing()
{

  // Question 9: compute FFT as before

  static bool init_done = false; /* initialization barrier */

  complex_t v[N], scratch[N];
  float Energy[N];
  float Sample;

  if (!init_done)
  {
    InitializeList(&SignalEntree, 0, N);
    ClearReal(v, N);
    init_done = true;
  }
  msg_box_receive(mbox, (char *)&Sample, true);

  Add_ElementList(&SignalEntree, Sample);

  sample_counter++; // Question 8: process samples only when N samples are collected

  if (sample_counter >= N)
  {
    sample_counter = 0; // Question 8: reset the counter for next window

    // Question 8: process the full window
    GetOrdereredList(&SignalEntree, &v[0]);
    ClearImaginary(v, N);
    fft(v, N, scratch);
    Computemodulus(v, N, Energy);
  }

  // Question 9: instead of printf, store results in a buffer and signal UART task that new data is available

  /* Display FFT result */

  for (int i = 0; i < N; i++)
  {
    printf("  %3.4f  ", Energy[i]);
  }
  printf("\n");
}

/******************************************************************************/
/* Signal storing */

void tStoreSignal()
{
  FILE *fp;
  int i;
  complex_t Sig[N];

  for (;;)
  {
    fp = fopen("./InputSignal.txt", "w+");
    GetOrdereredList(&SignalEntree, &Sig[0]);
    fp = fopen("./InputSignal.txt", "w+");
    for (i = 0; i < N; i++)
    {
      fprintf(fp, " \n %3.2f ", Sig[i].Re);
    }
    fprintf(fp, " \n");
    fclose(fp);
  }
}

/******************************************************************************/
/* main program entrypoint */

int main(int argc, char *argv[])
{
  printf(" FFT Demo ....\n");

  Time = 0.;
  pre_Time = 0.;

  /* Message box creation */

  mbox = msg_box_init(sizeof(float));

  /* Tasks creation */

  printf(" Creating the application tasks .... \n");

  struct timespec period_acquire = {0, ACQUIRE_PERIOD * 1000 * 1000};
  create_periodic_task(period_acquire, tAcquireSample);

  struct timespec period_processing = {0, PROCESSING_PERIOD * 1000 * 1000};
  create_periodic_task(period_processing, tProcessing);

  printf(" Tasks .. created and launched\n");

  /* Waiting for ctrl-c to stop the application */

  pause();

  printf(" Application ..... finished--> exit\n");

  return (EXIT_SUCCESS);
}
