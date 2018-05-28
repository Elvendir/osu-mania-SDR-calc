import numpy as np

power_kps = 2


def rms(list):
    return np.sqrt(np.mean(list ** 2))


def strange_invert_list(i_columns, list):
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


def calc_kps(kps_columns, i_columns, map):
    kps = [0]
    for i in range(1, len(map)):
        for k in range(len(i_columns[0])):
            if i_columns[i - 1][k] != i_columns[i][k]:
                kps.append(kps_columns[i][k])
    return kps


def calc_overall_difficulty(individual_difficulty, kps):
    return rms(individual_difficulty * kps ** power_kps)
