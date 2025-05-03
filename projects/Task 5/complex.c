#include <math.h>
#include "complex.h"
#include "utils.h"

/******************************************************************************/
void Computemodulus (complex_t * v, int n, float * Modulus) {
  float mod2, mod;
  int i;
  for (i = 0; i < n; i++) {
    mod2 = pow (v[i].Re, 2) + pow (v[i].Im, 2);
    mod = pow (mod2, 0.5);
    Modulus[i] = mod / (n * 0.5);
  }
  Modulus[0] = Modulus[0] / 2;
}

/******************************************************************************/
void ClearImaginary (complex_t * Complex_TNumber, int n) {
  for (int i = 0; i < n; i++) {
    Complex_TNumber[i].Im = 0;
  }
}

/******************************************************************************/
void ClearReal (complex_t * Complex_TNumber, int n) {
  for (int i = 0; i < n; i++) {
    Complex_TNumber[i].Re = 0;
  }
}

/******************************************************************************/
void fft (complex_t * v, int n, complex_t * tmp) {
  if (n > 1) {
    int k, m;
    complex_t z, w, *vo, *ve;
    ve = tmp;
    vo = tmp + n / 2;
    for (k = 0; k < n / 2; k++) {
      ve[k] = v[2 * k];
      vo[k] = v[2 * k + 1];
    }
    fft (ve, n / 2, v);
    /* FFT on even - indexed elements of v[] */
    fft (vo, n / 2, v);
    /* FFT on odd - indexed elements of v[] */
    for (m = 0; m < n / 2; m++) {
      w.Re = cos (2 * M_PI * m / (double)n);
      w.Im = -sin (2 * M_PI * m / (double)n);
      z.Re = w.Re * vo[m].Re - w.Im * vo[m].Im;
      z.Im = w.Re * vo[m].Im + w.Im * vo[m].Re;
      v[m].Re = ve[m].Re + z.Re;
      v[m].Im = ve[m].Im + z.Im;
      v[m + n / 2].Re = ve[m].Re - z.Re;
      v[m + n / 2].Im = ve[m].Im - z.Im;
    }
  }
}
