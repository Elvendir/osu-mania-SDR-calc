import numpy as np
import sys

'''
Stamina is taken into account by changing the base kps into a felt_kps.

For one note, felt_kps is thus the kps 'felt' when tired by playing :
felt_kps = G(all previous note's kps_felt and timing) * kps

With G a function (>= 1 ) encoding the reward given.

However, with this form G would be too complex (because would depends 2 * 'number_of_previous_notes' variables).
Thus, G is here the ideal reward function at constant kps : G(kps,t) (depends on only 2 variables).

And we maximise : G(min_kps,Delta_t) * min_kps : 
with min_kps a decreasing backward in time  from the note which stamina is calculated
    (exponential decay across all kps encountered)
and Delta_t  the time between the note and where tha calculation is backward in time 

(To see a visualisation of G uncomment in main.py the graph section)

All the constant below can be change to change the way stamina is rewarded. 
'''

kps_target = 5  # kps fixed for behavior of ideal reward function at constant kps : G
tau_target = 30  # typical time for reward, depending on structure of G and when stamina start to be greatly rewarded

tau_kps_mean = 15  # typical time of decay of kps_mean when searching for G_current_max, see calc_target


def G(kps, t):  # ideal reward for constant kps
    dif_kps = kps / kps_target
    norm = 10 * np.log(2)
    x = t / tau_target  # Normalized time

    return (np.log(x + 1) - np.log(x + 1) * np.exp(-x ** 2 * dif_kps ** 4)) / norm


def calc_next_felt_kps(kps, t, felt_kps, list_i, i):
    # Searches to maximize felt_kps with decreasing kps backward in time

    j = i
    kps_min = kps[list_i[i]]
    kps_mean = kps[list_i[i]]
    current_felt_kps = kps[list_i[i]]
    felt_kps[list_i[i]] = kps_min
    felt_kps_max = 0
    while j > 0 and (G(kps_min, t[list_i[i]] - t[0]) + 1) * kps_min > felt_kps_max:

        # Decreases kps backward in time
        Delta_t = t[list_i[j]] - t[list_i[j - 1]]
        kps_mean = kps_mean + (felt_kps[list_i[j]] - kps_mean) * Delta_t / tau_kps_mean
        if kps_mean < kps_min:
            if kps_mean < 0:
                kps_min = 0
            else:
                kps_min = kps_mean
        j -= 1

        # Calculates new fekt_kps
        G_ = G(kps_min, t[list_i[i]] - t[list_i[j]])
        current_felt_kps = (1 + G_) * kps_min
        if current_felt_kps >= felt_kps_max:
            felt_kps_max = current_felt_kps

    return felt_kps_max


def calc_felt_kps(map, list_i, kps, felt_kps, delay):
    t = map[:, 2] / 1000
    nb_notes = len(t)
    '''
    Time now in seconds !!!
    '''
    for i in range(1, len(list_i)):  # calculate felt_kps (> kps) because of stamina

        # A progress bar for the calculation
        if i % 100 == 0:
            sys.stdout.write("\r calc_stamina : " + str("%.0f" % (100 * (i + delay) / nb_notes)) + "%")
            sys.stdout.flush()

        current_felt_kps = calc_next_felt_kps(np.array(kps), t, felt_kps, np.array(list_i), i)
        felt_kps[list_i[i]] = current_felt_kps

    return np.array(felt_kps)
