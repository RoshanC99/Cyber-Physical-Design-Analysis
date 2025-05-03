#ifndef __LIST_H__
#define __LIST_H__

/*
 * This unit defines a circular queue list ADT. It will be used to store the
 * relevant bits of data when computing FFT/iFFT elements.
 */

/* Constants to statically dimension the list           */
#define q	4		/* for 2^q points       */
#define N	(1<<q)		/* N-point FFT, iFFT   */

/* Definition of the list */
typedef struct {
  float Array[N];
  int WritingIndex;
  int ReadingIndex;
  int ListLength;
}      list;

#include "complex.h"

void Add_ElementList (list * CircularQueue, float NewElement);
/* Add an element to the list */

void InitializeList (list * CircularQueue, float DefaultValue, int Length);
/* Initialize the list */

void PrintNotOrderedList (const char *title, list * CircularQueue);
void PrintOrderedList (const char *title, list * CircularQueue);
void GetOrdereredList (list * CircularQueue, complex_t * OrdereredList);

#endif				/* __LIST_H__ */
