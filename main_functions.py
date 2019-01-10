import numpy as np

'''
Useful functions
'''


power_kps = 2  # overall_difficulty power dependency on kps


def delete_LN_release(map):     # Deletes all LN's release
    k=0
    i=0
    n = len(map)
    while i+k<n:
        if map[i][1] == 2:
            map = np.delete(map, i, 0)
            k+=1
        else :
            i+=1
    return(map)


def rms(list, k):  # gives the k-root mean square of a np.array
    return pow(np.mean(list ** k), 1 / k)

def calc_overall_difficulty(individual_difficulty, kps):  # root mean square of ind_difficulty*kps^2
    return rms(individual_difficulty * kps ** power_kps)


