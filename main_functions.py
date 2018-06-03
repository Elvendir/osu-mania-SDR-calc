import numpy as np

power_kps = 2  # overall_difficulty power dependency on kps
LN_release_kps_correction = .07  # kps correction for LN release
LN_note_after_release_correction = .15  # kps correction for note after LN release


def rms(list , k):  # gives the root mean square of a np.array
  return pow(np.mean(list ** k),1/k)


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
        elif type[i_columns[i - 1][column]] == 2 :

            Delta_t = min((t[i] - t[i_columns[i - 1][column]] + LN_note_after_release_correction,
                           t[i] - t[i_columns[i_columns[i - 1][column] - 1][column]]))
        else:
            Delta_t = t[i] - t[i_columns[i - 1][column]]
        kps[column] = 1 / Delta_t
    return np.array(kps)


def build_patterns(type, column, t, patterns, nb_columns, current_t, j, i):
    if current_t == t[i]:
        patterns[j][column + 1] = type[i] + 1
        next_t = current_t
    else:
        j += 1
        patterns.append(np.array([0 for k in range(nb_columns + 1)]))
        for k in range(1, nb_columns + 1):
            if patterns[j - 1][k] == 2 or patterns[j - 1][k] == 4:
                patterns[j][k] = 4
        patterns[j][0] = t[i] - patterns[j - 1][0]
        patterns[j][column + 1] = type[i] + 1
        next_t = t[i]
    return (patterns, j, next_t)


def everything_useful(map, nb_columns):
    columns = map[:, 0]
    type = map[:, 1]
    t = map[:, 2]

    i_columns = [np.array([-1 for k in range(nb_columns)])]
    kps_columns = [np.array([0 for k in range(nb_columns)])]
    patterns = [np.array([0 for k in range(nb_columns + 1)])]
    j = 0
    i_to_j = [0]

    column = columns[0]
    i_columns[0][column] += 1
    patterns[0][column + 1] = type[0] + 1
    current_t = t[0]

    for i in range(1, len(map)):
        column = columns[i]
        i_columns.append(increment_i_column(i, i_columns, column))
        kps_columns.append(next_kps(i, i_columns, t / 1000, column, kps_columns, type))
        (patterns, j, current_t) = build_patterns(type, column, t, patterns, nb_columns, current_t, j, i)
        i_to_j.append(j)

    return (i_columns, kps_columns, patterns, i_to_j)


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


def columns_of_lin(kps, columns, nb_columns):
    kps_columns = [np.array([0. for k in range(nb_columns)])]
    kps_columns[0][columns[0]] = kps[0]
    for i in range(1, len(columns)):
        kps_columns.append(np.copy(kps_columns[i - 1]))
        kps_columns[i][columns[i]] = kps[i]
    return kps_columns


def lin_of_columns(kps_columns, columns):  # extract kps per from kps_columns
    kps = []
    for i in range(len(columns)):
        kps.append(kps_columns[i][columns[i]])
    return kps


def calc_overall_difficulty(individual_difficulty, kps):  # root mean square of ind_difficulty*kps^2
    return rms(individual_difficulty * kps ** power_kps)
