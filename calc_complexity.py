import numpy as np

'''
Reminder : type_note == 0 normal, 1 LN hold, 2 LN release
'''

multiple_hit_correction = [[-0.1, -0.05, +0],  # bonus/malus when multiple hit at once on same timing
                           [-0.05, -0.05, +0],  # lines : type of current note
                           [+0.05, +0.05, -0.05]]  # columns : type of other note at same timing

holding_correction = [+0.2, +0.2, +0.2]  # bonus when another note is hold, columns : type of current note


def calc_complexity_2_tp(pattern1, pattern0):
    complexity_2_tp = 0
    middle = int(np.ceil(len(pattern1) / 2))
    pattern_2_tp = np.array([pattern1, pattern0])
    pattern_2_tp_reversed = np.array([pattern0, pattern1])
    if np.array_equal(pattern1, pattern0):
        complexity_2_tp -= 0.05
    if np.array_equal(pattern1, pattern0[::-1]):
        complexity_2_tp -= 0.05
    if np.array_equal(pattern_2_tp[:middle], pattern_2_tp[middle:]):
        complexity_2_tp -= 0.05
    if np.array_equal(pattern_2_tp[:middle], pattern_2_tp_reversed[middle:]):
        complexity_2_tp -= 0.05
    return complexity_2_tp


def compression_correction(l1, l0):
    x = l1 / l0
    return x ** 2 / (1 + x ** 4)


def calc_complexity(map, i_to_j, patterns, columns):
    global_complexity = [1]
    complexity_patterns = [1]
    complexity_patterns.append(calc_complexity_2_tp(patterns[1, 1:], patterns[0, 1:]))
    global_complexity.append(calc_complexity_2_tp(patterns[1, 1:], patterns[0, 1:]))
    for j in range(2, i_to_j[len(columns) - 1] + 1):
        complexity_patterns.append(calc_complexity_2_tp(patterns[j, 1:], patterns[j - 1, 1:]))
        coef = compression_correction(patterns[j][0], patterns[j - 1][0])
        global_complexity.append((1 + complexity_patterns[j]) * (1 + coef * (global_complexity[j - 1] - 1)))
    global_complexity_i = []
    for i in range(len(i_to_j)):
        global_complexity_i.append(global_complexity[i_to_j[i]])
    return global_complexity_i
