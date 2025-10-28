#include <math.h>

#define PI2 2 * M_PI // pi * 2

typedef struct {
    float x[2]; // input x[n-1], x[n-2]
    float y[2]; // output y[n-1], y[n-2]
    float b0, b1, b2, a1, a2; // coeficientes do filtro
} BiquadFilter;

void init_notch_filter(BiquadFilter *filter_instance, float fs, float fc, float bw);
float apply_filter(BiquadFilter *filter_instance, float input);
