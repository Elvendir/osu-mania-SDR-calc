import numpy as np

power_kps = 2  # overall_difficulty power dependency on kps


def rms(list):  # gives the root mean square of a np.array
    return np.sqrt(np.mean(list ** 2))


def strange_invert_list(i_columns, list):
    # makes list_copy[i+1][k] be the value of list for the next note in column k
    # while list[i-1][k] still gives the value of list for the note before in column k
    # value after the last note of the column are fixed to 0 for list_copy
    list_copy = np.copy(np.array(list))
    for i in range(len(i_columns) - 2, 0, -1):
        if i == len(i_columns) - 2:
            for k in range(len(i_columns[0])):
                if i_columns[i - 1][k] == i_columns[i][k]:
                    list_copy[i][k] = 0
        else:
            for k in range(len(i_columns[0])):
                if i_columns[i - 1][k] == i_columns[i][k]:
                    list_copy[i][k] = list_copy[i + 1][k]
    return list_copy


def calc_kps(kps_columns, columns):  # extract kps per from kps_columns
    kps = [0]
    for i in range(1, len(columns)):
        kps.append(kps_columns[i][columns[i]])
    return kps


def calc_overall_difficulty(individual_difficulty, kps):  # root mean square of ind_difficulty*kps^2
    return rms(individual_difficulty * kps ** power_kps)
