import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as col

'''
An FFT (Discrete Fourier Transform) is done on a sample of the map.

Sample_length : sample_size in number and sample_size*TF_time_scale in ms
Sample_width : nb_columns + space_btw_columns*(nb_columns-1)

Complexity is calculated by a sum over the absolute value of Fourier' s coefficient. 
(Maybe will select only some frequencies later for a more precise complexity.)
'''

TF_time_scale = 1  # Length in ms of a pixel of the sample
sample_size = 1000  # Number of pixel for sample length
note_placement = 499  # Placement of the note (for which complexity is calculated) inside the sample
# (0 will put it at the bottom of the sample and sample_size - 1 will put it at the top )
# And currently doesn't work LOL

space_btw_columns = 10  # Pixels of void between each columns for a more precise FFT


def initialize_sample(nb_columns):
    sample = []
    for i in range(sample_size):
        sample.append(np.array([0 for k in range(nb_columns + space_btw_columns * (nb_columns - 1))]))
    return sample


def create_sample(t, columns, i_min, sample):  # Creates the first sample
    i = 0
    j = 0
    nb_notes_sample = 0
    t_max = (sample_size - note_placement - 1) * TF_time_scale
    t_min = -TF_time_scale * note_placement
    i = i_min
    i_min_next = i_min
    while i < len(t) and t[i] <= t_max:
        if t[i] < t_min:
            i_min_next += 1
        else:
            placement = int(note_placement + t[i] / TF_time_scale)
            sample[placement][columns[i] * space_btw_columns] = 1
            nb_notes_sample += 1
        i += 1

    return sample, nb_notes_sample, i_min_next


def calc_complexity(map, nb_columns, kps):  # Calculates FFT and complexity of all notes
    delta_i = 100
    delta_j = 0
    nu = 0
    last_j = 0
    i = 0
    i_min = 0
    complexity = []
    t = np.copy(map[:, 2])
    columns = map[:, 0]
    nb_notes = len(t)
    sample = initialize_sample(nb_columns)
    while i < len(t):
        t -= t[i]
        (fft_sample, nb_notes_sample, i_min) = create_sample(t, columns, i_min, sample)

        a_sample = np.array(sample)
        fft_sample = abs(np.fft.rfft2(a_sample))

        # Currently complexity is just the sum of the absolute value of FFT' s coefficients
        base_complexity = np.sum(fft_sample)
        next_complexity = base_complexity - np.sum(fft_sample[0, 0])
        next_complexity = next_complexity / (
                np.sqrt(nb_notes_sample) * sample_size * (nb_columns + (nb_columns - 1) * space_btw_columns))
        while i < len(t) and t[i] == 0:
            complexity.append(next_complexity)
            i += 1
            delta_i += 1

        # A progress bar for the calculation
        if delta_i > 100:
            delta_i = 0
            sys.stdout.write("\r calc_complexity : " + str("%.0f" % (100 * i / nb_notes)) + "%")
            sys.stdout.flush()

        '''
        # Uncomment to have a FFT and pattern visualisation every 10000*TF_time_scale of the map
        # And tweak conditions to choose for which complexity
        delta_j = - last_j + j
        kps_mm = kps[i-1]
        if delta_j > 0:
            if next_complexity < 1 and kps_mm > 9  :
                nu += 1
                last_j = j
                plt.figure()
                norm = col.Normalize()
                plt.subplot(2, 1, 1)
                plt.title("Pattern with " + str("%.2f" % next_complexity) + " complexity")
                plt.pcolor(np.swapaxes(a_sample,0,1), norm=norm)
                norm = col.Normalize()
                plt.subplot(2, 1, 2)
                plt.title("FFT visualisation at " + str("%.2f" % (t[i-1]/1000) ) + " s")
                plt.pcolor(np.swapaxes(abs_fft_sample,0,1), norm=norm)
        if nu == 10 :
            nu = 0
            plt.show()
        '''

    return complexity
