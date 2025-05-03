#ifndef __COMPLEX_H__
#define __COMPLEX_H__

typedef struct {
  float Re;
  float Im;
}      complex_t;

void Computemodulus (complex_t * v, int n, float *Modulus);
void ClearImaginary (complex_t * Complex_TNumber, int n);
void ClearReal (complex_t * Complex_TNumber, int n);
void fft (complex_t * v, int n, complex_t * tmp);

#endif				/* __COMPLEX_H__ */
