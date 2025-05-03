#include <stdio.h>
#include "list.h"

/******************************************************************************/
void Add_ElementList (list * CircularQueue, float NewElement) {
  CircularQueue->Array[CircularQueue->WritingIndex] = NewElement;
  CircularQueue->ReadingIndex = CircularQueue->WritingIndex;
  CircularQueue->WritingIndex++;

  if (CircularQueue->WritingIndex > CircularQueue->ListLength - 1) {
    CircularQueue->WritingIndex = 0;
  }
}
/******************************************************************************/
void InitializeList (list * CircularQueue, float DefaultValue, int Length) {
  int i;
  CircularQueue->WritingIndex = 0;
  CircularQueue->ListLength = Length;
  for (i = 0; i < CircularQueue->ListLength; i++) {
    CircularQueue->Array[i] = DefaultValue;
  }
}

/******************************************************************************/
void PrintNotOrderedList (const char *title, list * CircularQueue) {
  int i;
  printf ("%s %d ", title, CircularQueue->ListLength);
  for (i = 0; i < CircularQueue->ListLength; i++) {
    printf ("#%d: %3.2f ", i, CircularQueue->Array[i]);
  }
  printf ("\n");
}

/******************************************************************************/
void PrintOrderedList (const char *title, list * CircularQueue) {
  int i, cpt;
  i = CircularQueue->WritingIndex;

  for (cpt = 0; cpt < CircularQueue->ListLength; cpt++) {
    printf (" : %3.2f", CircularQueue->Array[i]);
    i++;
    if (i >= CircularQueue->ListLength) {
      i = 0;
    }
  }
  printf ("\n");
}
/******************************************************************************/
void GetOrdereredList (list * CircularQueue, complex_t * OrdereredList) {
  int i, cpt;
  float data;
  i = CircularQueue->WritingIndex;

  for (cpt = 0; cpt < CircularQueue->ListLength; cpt++) {
    data = CircularQueue->Array[i];
    OrdereredList[cpt].Re = data;
    i++;
    //printf (" %3.2f ", data);
    if (i >= CircularQueue->ListLength) {
      i = 0;
    }
  }
}
