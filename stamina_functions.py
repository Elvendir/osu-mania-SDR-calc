import numpy as np

'''
All the constant below can be change to change the way stamina is rewarded 
and to tweak kps value because of LN release. 
'''

LN_release_kps_correction = .05  # kps correction for LN release
LN_note_after_release_correction = .1  # kps correction for note after LN release

kps_target = 5  # kps fixed for behavior of ideal reward function at constant kps : G
tau_target = 60  # typical time for reward, depending on structure of G and when stamina start to be greatly rewarded

tau_kps_mean = 7  # typical time of decay of kps_mean when searching for G_current_max, see calc_target
tau_higher = 10  # typical time of recovery rate, 1/(decay rate) of s_rewarded when s_rewarded > G_current
tau_lower = 1  # typical time of convergence when s_rewarded < G_current,
# need to be low for following G but not too much because of discretization problems
tau_s_memory = 20  # typical time of recovery rate from none 0 past stamina before new section


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
    return 0.5 * (pow(t / tau_target + 1, kps ** 2 / kps_target ** 2 + 1) - (t / tau_target + 1))


def d_G(kps, t):  # derivative of G
    return (kps ** 2 / kps_target ** 2 + 1) * (0.5 / tau_target) * pow(t / tau_target + 1,
                                                                       kps ** 2 / kps_target ** 2) - 0.5 / tau_target


def calc_target(kps, t, s, list_i, i):  # searching to maximize s_targeted with decreasing kps backward im time
    j = i
    j_max = list_i[j - 1]
    kps_min = kps[i]
    s_targeted = 0
    s_targeted_max = 0
    dg = 0
    dg_max = 0
    kps_mean = kps[i]

    while list_i[j - 1] > 0 and G(kps_min, t[i] - t[0]) > s_targeted_max:
        Delta_t = t[j] - t[list_i[j - 1]]
        kps_mean = kps_mean + (kps[j] - kps_mean) * Delta_t / tau_kps_mean  # dif eq for kps_mean
        if kps_mean <= kps_min:
            kps_min = kps_mean  # using as kps in G and d_G the lowest kps_mean encountered
        j = list_i[j - 1]
        s_targeted = G(kps_min, t[i] - t[j])
        if s_targeted >= s_targeted_max:
            s_targeted_max = s_targeted
            j_max = j
        dg = d_G(kps_min, t[i] - t[j])
        if dg > dg_max:
            dg_max = dg
    s_targeted_max += s[j_max] * np.exp((t[j_max] - t[i]) / tau_s_memory)  # adding the stamina memory term
    return (s_targeted_max, dg_max)


def dif_eq(kps, t, s, list_i, i):  # apply discrete differential equation as discussed in the overleaf
    i_m1 = list_i[i - 1]
    Delta_t = t[i] - t[i_m1]
    (s_targeted, dg) = calc_target(kps, t, s, list_i, i)
    if s[i_m1] > s_targeted:
        next_s = s[i_m1] + dg * Delta_t + (s_targeted - s[i_m1]) * Delta_t / tau_higher
        if next_s > 0:
            return next_s
        else:
            return 0
    else:
        next_s = s[i_m1] + dg * Delta_t + (s_targeted - s[i_m1]) * Delta_t / tau_lower
        if next_s > 0:
            return next_s
        else:
            return 0
