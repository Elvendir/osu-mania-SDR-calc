import numpy as np


'''
All the constant below can be change to change the way stamina is rewarded 
and to tweak kps value because of LN release. 
'''

kps_target = 5  # kps fixed for behavior of ideal reward function at constant kps : G
tau_target = 30  # typical time for reward, depending on structure of G and when stamina start to be greatly rewarded

tau_kps_mean = 30  # typical time of decay of kps_mean when searching for G_current_max, see calc_target


def G(kps, t):  # ideal reward for constant kps
    dif_kps = kps / kps_target
    norm = 10 * np.log(2)
    x = t / tau_target
    return (np.log(x + 1) - np.log(x + 1) * np.exp(-x ** 2 * dif_kps ** 4)) / norm


def calc_next_felt_kps(kps, t, felt_kps, list_i,
                       i):  # searching to maximize felt_kps with decreasing kps backward im time
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


def calc_felt_kps_stamina(map, i_columns, kps_columns):
    t = map[:, 2] / 1000
    '''
    Time now in seconds !!!
    '''
    columns = map[:, 0]
    felt_kps = [0]
    nb_columns = len(i_columns[0])

    for i in range(1, len(map)):  # calculate felt_kps > kps because of stamina
        column = columns[i]
        if i_columns[i - 1][column] == -1:
            felt_kps.append(0)
            # if first note of the column felt_kps == 0
        else:
            current_felt_kps = calc_next_felt_kps(np.array(kps_columns)[:, column], t, felt_kps,
                                                  np.array(i_columns)[:, column], i)
            felt_kps.append(current_felt_kps)
    return np.array(felt_kps)

'''
    kps_columns_inverted = strange_invert_list(i_columns, kps_columns)
    # makes kps_columns_inverted[i+1][k] be the value of kps for the next note in column k
    # while kps_columns[i-1][k] still gives the value of kps for the note before in column k
    # value after the last note of the column are fixed to 0 for kps_columns_inverted

    rho = [0]
    felt_rho = [0]
    trivial_list = [k for k in range(len(t))]

    for i in range(1, len(map)):  # calculate global stamina
        kps_columns_same_timing_xor_next = []
        for k in range(nb_columns):
            if t[i_columns[i][k]] == t[i]:
                kps_columns_same_timing_xor_next.append(kps_columns[i][k])
            else:
                kps_columns_same_timing_xor_next.append(kps_columns_inverted[i][k])
        rho.append(rms(np.array(kps_columns_same_timing_xor_next)))
        # rho is the 'kps_density' calculate with a rms of the kps of each column
        # the kps used is the one of note with same timing point and if there isn't the kps of next one in the column
        current_felt_rho = calc_next_felt_kps(rho, t, felt_rho, trivial_list, i)
        felt_rho.append(current_felt_rho)

    kps = calc_kps(kps_columns, columns)
    coef = []
    for i in range(len(map)):
        if kps[i] == 0:
            coef.append(0)
        else:
            coef.append(0.5 * np.sqrt(nb_columns - 1) * (felt_rho[i] / rho[i] - 1) + felt_kps[i] / kps[i])
'''

