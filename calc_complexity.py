import numpy as np
import sys
import matplotlib.pyplot as plt

'''
An FFT (Discrete Fourier Transform) is done on a sample of the map.

Sample_length : sample_size in number and sample_size*TF_time_scale in ms
Sample_width : nb_columns + space_btw_columns*(nb_columns-1)

Complexity is calculated by a sum over the absolute value of Fourier' s coefficient. 
(Maybe will select only some frequencies later for a more precise complexity.)
'''

TF_time_scale = 1  # Length in ms of a pixel of the sample
sample_size = 2000  # Number of pixel for sample length
note_placement = 999  # Placement of the note (for which complexity is calculated) inside the sample
# (0 will put it at the bottom of the sample and sample_size - 1 will put it at the top )
space_btw_columns = 10  # Pixels of void between each columns for a more precise FFT


def create_array(map, nb_columns):  # Creates the first sample
    sample = []
    t = map[:, 2]
    column = map[:, 0]
    for i in range(sample_size):
        sample.append(np.array([0 for k in range(nb_columns + space_btw_columns * (nb_columns - 1))]))
    i = 0
    j = 0
    tc = t[0] + (j + note_placement) * TF_time_scale
    while t[i] <= tc:
        sample[note_placement][column[i] * space_btw_columns] = 1
        i += 1
    j = 1
    return sample, j, i


def increment_array(sample, j, i, map, nb_columns):  # Creates next sample
    t = map[:, 2]
    column = map[:, 0]
    nb_note = 0  # Needed to count number of notes placed on the same line in time (2 notes or more at same time)
    tc = t[0] + (j + note_placement) * TF_time_scale
    while t[i] > tc:
        j += 1
        sample.pop(0)
        sample.append(np.array([0 for k in range(nb_columns + space_btw_columns * (nb_columns - 1))]))
        tc += TF_time_scale

    while i < len(map) and t[i] <= tc:
        sample[note_placement][column[i] * space_btw_columns] = 1
        nb_note += 1
        i += 1
    return sample, j, i, nb_note


def calc_complexity(map, nb_columns):  # Calculates FFT and complexity of all notes
    delta_j = 0
    last_j = 0
    complexity = []
    base_complexity_l = []
    t = map[:, 2]
    nb_notes = len(t)

    # First sample and complexity calculation
    (sample, j, i) = create_array(map, nb_columns)
    a_sample = np.array(sample)
    fft_sample = abs(np.fft.rfft2(a_sample))
    for k in range(i):  # Add a complexity for each note on same timeline
        base_complexity = np.sum(fft_sample)
        next_complexity = base_complexity - np.sum(fft_sample[:, 0]) - np.sum(fft_sample[0, :])
        next_complexity = next_complexity / (sample_size * (nb_columns + (nb_columns - 1) * space_btw_columns))
        base_complexity = base_complexity / (sample_size * (nb_columns + (nb_columns - 1) * space_btw_columns))

        base_complexity_l.append(base_complexity)
        complexity.append(next_complexity)
        # Currently complexity is just the sum of the absolute value of FFT' s coefficients

    while i < len(map):

        # A progress bar for the calculation
        if i % 100 == 0:
            sys.stdout.write("\r calc_complexity : " + str("%.0f" % (100 * i / nb_notes)) + "%")
            sys.stdout.flush()

        (sample, j, i, nb_note) = increment_array(sample, j, i, map, nb_columns)

        a_sample = np.array(sample)
        fft_sample = np.fft.rfft2(a_sample)
        abs_fft_sample = abs(fft_sample)
        for k in range(nb_note):
            base_complexity = np.sum(abs_fft_sample)
            next_complexity = base_complexity - np.sum(abs_fft_sample[0, :]) + abs_fft_sample[0, 0]
            next_complexity = next_complexity / (sample_size * (nb_columns + (nb_columns - 1) * space_btw_columns))
            base_complexity = base_complexity / (sample_size * (nb_columns + (nb_columns - 1) * space_btw_columns))

            base_complexity_l.append(base_complexity)
            complexity.append(next_complexity)
        '''
        # Uncomment to have a FFT visualisation every 10000*TF_time_scale  of the map
        delta_j = - last_j + j
        if delta_j > 10000 :
            last_j = j
            tc = t[0] + (j + note_placement) * TF_time_scale
            plt.plot(fft_sample[:,0])
            plt.title("FFT at " + str("%.3f" % (tc/1000) + "s into the song."))
            plt.show()
        '''
    return complexity
