import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import codecs
import glob
import time
from main_functions import *
from map_extraction import *
from calc_stamina import calc_felt_kps_stamina
from calc_complexity import calc_complexity

'''
Calculate difficulty for each .osu file in folder_path
Write all song_name;difficulty in a DATA file
'''

g = codecs.open('DATAs', 'w', 'utf-8')
print('Folder with only .osu files')
folder_path = input()

for element in os.listdir(folder_path):
    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element

    (map, nb_columns) = extract_info(file_path)
    (i_columns, kps_columns, patterns, i_to_j) = everything_useful(map, nb_columns)
    columns = map[:, 0]
    kps = lin_of_columns(kps_columns, columns)
    complexity = np.array(calc_complexity(map, i_to_j, np.array(patterns), columns))
    print(name)
    print(rms(complexity))
    g.write(name + ';' + str(rms(complexity))+'\n')
    '''
    felt_kps_columns = columns_of_lin(felt_kps, columns, nb_columns)
    felt_kps = calc_felt_kps_stamina(map, i_columns, kps_columns)
    felt_kps = np.array(complexity)*np.array(kps)

    overall_difficulty = rms(np.array(felt_kps) ** 2)
    rms_kps_2 = rms(np.array(kps) ** 2)

    g.write(name + ';' + str(overall_difficulty) + '\n')
    print('dif = ' + str(overall_difficulty) + '; rms_kps = ' + str(
        rms_kps_2) + '; name = ' + name + '; nb_note = ' + str(
        len(columns)) + '; calc_time = ' + str(
        time.time() - t0))
    '''
g.close()
