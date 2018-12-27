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
from plot_graphs import *

'''
Calculate difficulty for each .osu file in folder_path
Write all song_name;difficulty in a DATA file
'''

g = codecs.open('DATAs', 'w', 'utf-8')
print('Folder with only .osu files')
folder_path = input()
g.write('name;nb_column;true_nb_columns;dif \n')
for element in os.listdir(folder_path):
    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element
    (map, nb_columns, true_nb_columns) = extract_info(file_path)
    map=delete_LN_release(map)
    (kps, left_i, right_i) = calc_kps(map, nb_columns)

    felt_kps = [0 for i in range(len(map))]
    felt_kps = calc_felt_kps_stamina(map, left_i, kps, felt_kps)
    felt_kps = calc_felt_kps_stamina(map, right_i, kps, felt_kps)

    overall_difficulty = np.mean(np.array(felt_kps))
    mean_kps = np.mean(np.array(kps))
    g.write(name)
    g.write(';' + str(nb_columns))
    g.write(';' + str(true_nb_columns))
    g.write(';' + str(mean_kps))
    g.write(';' + str(overall_difficulty) + '\n')
    print('dif = ' + str(overall_difficulty) + '; mean_complexity ='  + '; mean_kps = ' + str(
        mean_kps) + '; name = ' + name + '; nb_note = ' + str(
        len(map)) + '; calc_time = ' + str(
        time.time() - t0) + '; nb_columns = ' + str(nb_columns) + '; true_nb =' + str(true_nb_columns))
    plot_kps_felt_kps_graphics(name,left_i,right_i,kps,felt_kps,map[:,2])

plt.show()
g.close()
