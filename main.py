import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import codecs
import glob
import time
from main_functions import *
from map_extraction import *
from calc_stamina import *
from calc_complexity import *
from plot_graphs import *

'''
Calculate difficulty for each .osu file in folder_path
Write all song_name;difficulty in a DATA file
And plot graphs : 
    stamina_local/global and kps vs time per column
    complexity and stamina_total and individual_difficulty vs time
'''

g = codecs.open('DATAs', 'w', 'utf-8')
print('Folder with only .osu files')
folder_path = input()

for element in os.listdir(folder_path):
    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element
    (map, nb_columns) = extract_info(file_path)
    columns = map[:, 0]
    (stamina, kps_columns, i_columns, rho, s_local, s_local_max, s_global, s_global_max) = calc_stamina(map, nb_columns)
    complexity = calc_complexity(i_columns, map, nb_columns)
    kps = calc_kps(kps_columns, columns)

    overall_difficulty = calc_overall_difficulty(np.array(stamina) * np.array(complexity), np.array(kps))
    rms_kps = rms(np.array(kps) ** 2)

    g.write(name + ';' + str(overall_difficulty) + '\n')
    print(name + '; dif = ' + str(overall_difficulty) + '; rms_kps = ' + str(rms_kps) + '; nb_note = ' + str(
        len(columns)) + '; calc_time = ' + str(
        time.time() - t0))
    t = map[:, 2] / 1000
    plot_staminas_kps_graphics(name, nb_columns, i_columns, kps_columns, rho, s_local, s_local_max, s_global,
                               s_global_max, t)
    plot_stamina_complexity(np.array(stamina), np.array(complexity), t)

plt.show()
g.close()
