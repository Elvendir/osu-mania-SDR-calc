import numpy as np
from main_functions import *

'''
Reminder : type_note == 0 normal, 1 LN hold, 2 LN release
'''

multiple_hit_correction = [[-0.05, -0.05, +0],  # bonus/malus when multiple hit at once on same timing
                           [-0.05, -0.05, +0],  # lines : type of current note
                           [+0.05, +0.05, -0.05]]  # columns : type of other note at same timing

holding_correction = [+0.2, +0.2, +0.2]  # bonus when another note is hold, columns : type of current note


def calc_complexity(i_columns, map, nb_columns):
    complexity = [1]
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
                    # when true i_k is the id_note of the note before i in column k
                    # and i_k_inv is the id_note of the note after i in column k
                    if t[i_k] == t[i]:
                        individual_complexity += multiple_hit_correction[type[i]][type[i_k]]
                    elif t[i_k_inv] == t[i]:
                        individual_complexity += multiple_hit_correction[type[i]][type[i_k_inv]]
                    else:
                        if type[i_k] == 1:
                            individual_complexity += holding_correction[type[i]]
        complexity.append(individual_complexity)
    return complexity
