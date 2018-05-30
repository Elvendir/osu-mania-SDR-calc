import numpy as np

'''
All the constant below can be change to change the way stamina is rewarded 
and to tweak kps value because of LN release. 
'''

LN_release_kps_correction = .05  # kps correction for LN release
LN_note_after_release_correction = .1  # kps correction for note after LN release

kps_target = 5  # kps fixed for behavior of ideal reward function at constant kps : G
tau_target = 30  # typical time for reward, depending on structure of G and when stamina start to be greatly rewarded

tau_kps_mean = 30  # typical time of decay of kps_mean when searching for G_current_max, see calc_target


def increment_i_column(i, i_columns, column):
    # create the i-th i_columns element
    # i_columns structured: for i in column k, i_columns[i-1][k] gives note_id of the note before i in k column
    # when first note of column i == 0 xor i_columns[i-1][k] == -1
    current_i_columns = [i_columns[i - 1][k] for k in range(len(i_columns[i - 1]))]
    current_i_columns[column] = i
    return np.array(current_i_columns)


def next_kps(i, i_columns, t, column, kps_columns, type):
    # same as increment_i_columns but for kps_columns with kps calculation
    kps = [kps_columns[i - 1][k] for k in range(len(kps_columns[i - 1]))]
    if i_columns[i - 1][column] != -1:
        # kps calculation with correction depending note_type and note_before_type
        if type[i] == 2:
            Delta_t = t[i] - t[i_columns[i - 1][column]] + LN_release_kps_correction
            kps[column] = 1 / Delta_t
        if type[i_columns[i - 1][column]] == 2:
            Delta_t = max((t[i] - t[i_columns[i - 1][column]] + LN_release_kps_correction,
                           t[i] - t[i_columns[i_columns[i - 1]][column]]))
            kps[column] = 1 / Delta_t
        else:
            Delta_t = t[i] - t[i_columns[i - 1][column]]
            kps[column] = 1 / Delta_t
    return np.array(kps)


def G(kps, t):  # ideal reward for constant kps
    dif_kps = kps / kps_target
    norm = 10 * np.log(2)
    x = t / tau_target
    return (np.log(x + 1) - np.log(x + 1) * np.exp(-x ** 2 * dif_kps ** 4)) / norm


def calc_kps_felt(kps, t, felt_kps, list_i, i):  # searching to maximize felt_kps with decreasing kps backward im time
    j = i
    j_max = list_i[j - 1]
    kps_min = kps[i]
    kps_mean = kps[i]
    felt_kps.append(kps[i])
    current_felt_kps = kps[i]
    felt_kps_max = 0
    while list_i[j - 1] > 0 and (G(kps_min, t[i] - t[0]) + 1) * kps_min > felt_kps_max:
        Delta_t = t[j] - t[list_i[j - 1]]
        kps_mean = kps_mean + (felt_kps[j] - kps_mean) * Delta_t / tau_kps_mean
        if kps_mean < kps_min:
            if kps_mean < 0:
                kps_min = 0
            else:
                kps_min = kps_mean
        j = list_i[j - 1]
        G_ = G(kps_min, t[i] - t[j])
        current_felt_kps = (1 + G_) * kps_min
        if current_felt_kps >= felt_kps_max:
            felt_kps_max = current_felt_kps
    trashh = felt_kps.pop()
    return felt_kps_max
