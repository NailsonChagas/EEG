#include "filter.h"

void init_notch_filter(BiquadFilter *filter_instance, float fs, float fc, float bw)
{
	// https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html
	// y[n] = (b0/a0)*x[n] + (b1/a0)*x[n-1] + (b2/a0)*x[x-2] - (a1/a0)*y[n-1] - (a2/a0)*y[n-2]
	float omega_0 = PI2 * (fc/fs);
	float sin_omega = sin(omega_0);
	float cos_omega = cos(omega_0);
	float alpha = sin_omega * sinh( (log(2.0) / 2.0) * bw * omega_0 / sin_omega );
	float a0 =  1.0f + alpha;

	filter_instance->b0 = 1.0f / a0;
	filter_instance->b1 = (-2.0f * cos_omega) / a0;
	filter_instance->b2 = 1.0f / a0;
	filter_instance->a1 = (-2.0f * cos_omega) / a0;
	filter_instance->a2 = (1.0f - alpha) / a0;
}

float apply_filter(BiquadFilter *filter_instance, float input)
{
	// Faltando pesquisar como usar instruções ARM MAC
	float output = (filter_instance->b0 * input) + (filter_instance->b1 * filter_instance->x[0])
		+ (filter_instance->b2 * filter_instance->x[1]) - (filter_instance->a1 * filter_instance->y[0])
		- (filter_instance->a2 * filter_instance->y[1]);

	filter_instance->x[1] = filter_instance->x[0];
	filter_instance->x[0] = input;
	filter_instance->y[1] = filter_instance->y[0];
	filter_instance->y[0] = output;

	return output;
}
