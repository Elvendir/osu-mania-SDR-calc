import numpy as np
from stamina_functions import *
from main_functions import *


def calc_stamina(map, nb_columns):
    t = map[:, 2] / 1000
    '''
    Time now in seconds !!!
    '''
    type = map[:, 1]
    s_local = [0]
    s_local_max = [0]
    s_global = [0]
    s_global_max = [0]

    i_columns = [np.array([-1 for k in range(nb_columns)])]
    # i_columns structure: for i in column k, i_columns[i-1][k] gives note_id of the note before i in k column
    # if no note before in column k and i!= 0, i_columns[i-1][k] = -1
    kps_columns = [np.array([0 for k in range(nb_columns)])]
    # kps_columns structure: for i in column k, kps_columns[i-1][k] gives kps_note of the note before i in k column
    # if first note of column kps == 0
    rho = [0]

    column = map[0][0]
    i_columns[0][column] += 1  # init i_columns with first note

    trivial_list = [k for k in range(len(map))]  # used instead of i_columns[:,k] for global_stamina

    for i in range(1, len(map)):  # calculate local stamina
        column = map[i][0]
        i_columns.append(increment_i_column(i, i_columns, column))
        kps_columns.append(next_kps(i, i_columns, t, column, kps_columns, type))

        if i_columns[i - 1][column] == -1:
            s_local.append(0)
            s_local_max.append(0)
            # if first note of the column s_local == 0
        else:
            (current_s, current_s_max) = dif_eq(np.array(kps_columns)[:, column], t, s_local,
                                                np.array(i_columns)[:, column], i)
            s_local.append(current_s)
            s_local_max.append(current_s_max)

    kps_columns_inverted = strange_invert_list(i_columns, kps_columns)
    # makes kps_columns_inverted[i+1][k] be the value of kps for the next note in column k
    # while kps_columns[i-1][k] still gives the value of kps for the note before in column k
    # value after the last note of the column are fixed to 0 for kps_columns_inverted

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
        (current_s, current_s_max) = dif_eq(rho, t, s_global, trivial_list, i)
        s_global.append(current_s)
        s_global_max.append(current_s_max)

    stamina_total = 1 + np.array(s_local) + np.sqrt(nb_columns - 1) * np.array(s_global) / 4  # formula for s_total
    return (stamina_total, kps_columns, i_columns, rho, s_local, s_local_max, s_global, s_global_max)
