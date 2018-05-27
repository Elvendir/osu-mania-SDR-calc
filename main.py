import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import codecs
import glob
import time
from main_functions import *
from calc_stamina import *
from map_extraction import *
from plot_graphs import *

print('Folder with only .osu files')
folder_path = input()
g = codecs.open('DATAs', 'w', 'utf-8')

songs_new_difficulty = []
songs_osu_difficulty = []

for element in os.listdir(folder_path):
    file_path = folder_path + '/' + element
    name = element
    (map, nb_columns) = extract_info(file_path)

    (stamina, kps_columns, i_columns) = calc_stamina(map, nb_columns)

    kps = calc_kps(kps_columns, i_columns, map, rho, s_local, s_local_max, s_global, s_global_max)
    overall_difficulty = calc_overall_difficulty(np.array(stamina), np.array(kps))
    g.write(name + ';' + str(overall_difficulty) + '\n')
    songs_new_difficulty.append(overall_difficulty)
    plot_stamina_kps_graphics(name, nb_columns, i_columns, kps_columns, rho, s_local, s_local_max, s_global,
                              s_global_max)
plt.plot(songs_osu_difficulty, songs_new_difficulty, '+')
g.close()
