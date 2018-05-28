import numpy as np
from main_functions import *

multiple_hit_correction = [[-0.05, -0.05, +0],
                           [-0.05, -0.05, +0],
                           [+0.05, +0.05, -0.05]]
holding_correction = [+0.1, +0.1, -0.2]


def calc_complexity(i_columns, map, nb_columns):
    complexity = [0]
    i_columns_inverted = strange_invert_list(i_columns, i_columns)
    for i in range(1, len(map)):
        t = map[:, 2]
        type = map[:, 1]
        individual_complexity = 1
        if i != 0:
            for k in range(nb_columns):
                i_k = i_columns[i][k]
                i_k_inv = i_columns_inverted[i][k]
                if i_k != i:
                    if t[i_k] == t[i]:
                        individual_complexity += multiple_hit_correction[i][i_k]
                    elif t[i_k_inv] == t[i]:
                        individual_complexity += multiple_hit_correction[i][i_k_inv]
                    else:
                        if type[i_k] == 1:
                            individual_complexity += holding_correction[i]
        complexity.append(individual_complexity)
    return complexity
