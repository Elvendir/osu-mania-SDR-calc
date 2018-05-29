import numpy as np
from stamina_functions import *
from main_functions import *


def calc_stamina(map, nb_columns):
    t = map[:, 2] / 1000
    '''
    Time now in seconds !!!
    '''
    type = map[:, 1]
    felt_kps = [0]

    i_columns = [np.array([-1 for k in range(nb_columns)])]
    # i_columns structure: for i in column k, i_columns[i-1][k] gives note_id of the note before i in k column
    # if no note before in column k and i!= 0, i_columns[i-1][k] = -1
    kps_columns = [np.array([0 for k in range(nb_columns)])]
    # kps_columns structure: for i in column k, kps_columns[i-1][k] gives kps_note of the note before i in k column
    # if first note of column kps == 0
    # rho = [0]

    column = map[0][0]
    i_columns[0][column] += 1  # init i_columns with first note

    for i in range(1, len(map)):  # calculate felt_kps > kps because of stamina
        column = map[i][0]
        i_columns.append(increment_i_column(i, i_columns, column))
        kps_columns.append(next_kps(i, i_columns, t, column, kps_columns, type))

        if i_columns[i - 1][column] == -1:
            felt_kps.append(0)
            # if first note of the column felt_kps == 0
        else:
            current_felt_kps = calc_kps_felt(np.array(kps_columns)[:, column], t, felt_kps,
                                             np.array(i_columns)[:, column], i)
            felt_kps.append(current_felt_kps)

    return (felt_kps, kps_columns, i_columns)
