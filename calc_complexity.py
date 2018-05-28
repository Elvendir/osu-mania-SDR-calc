import numpy as np
from main_functions import *

def calc_complexity (i_columns,map,nb_columns) :
    complexity = [0]
    i_columns_inverted = strange_invert_list(i_columns,i_columns)
    for i in range(1,len(map)):
        t = map[:,2]
        type = map[:,1]
        individual_complexity = 1
        if i != 0:
            for k in range(nb_columns) :
                i_k = i_columns[i][k]
                i_k_inv = i_columns_inverted[i][k]
                if i_k != i:
                    if t[i_k] == t[i] :
                        if type[i_k] == 1 or type[i_k] == 0 :
                            if type[i] == 2 :
                                individual_complexity += 0.05
                            else :
                                individual_complexity -= 0.05
                    elif t[i_k_inv] == t[i] :
                        if type[i_k_inv] == 1 or type[i_k_inv] == 0 :
                            if type[i] == 2 :
                                individual_complexity += 0.05
                            else :
                                individual_complexity -= 0.05
                    else :
                        if type[i_k] == 1 :
                            if type[i] == 0 :
                                individual_complexity += 0.10
                            elif type[i] == 1 :
                                individual_complexity += 0.20
                            else:
                                individual_complexity += 0.20
        complexity.append(individual_complexity)
    return complexity