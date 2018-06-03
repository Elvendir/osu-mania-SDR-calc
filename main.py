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
g.write('name;nb_column;true_nb_columns;mean1 dif;mean1 kps;mean2 dif;mean2 kps;mean3 dif;mean3 kps;mean4 dif;mean4 kps;mean5 dif;mean5 \n')
for element in os.listdir(folder_path):
    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element

    (map, nb_columns, true_nb_columns) = extract_info(file_path)
    (i_columns, kps_columns, patterns, i_to_j) = everything_useful(map, nb_columns)
    columns = map[:, 0]
    kps = lin_of_columns(kps_columns, columns)
    felt_kps = calc_felt_kps_stamina(map, i_columns, kps_columns)

    g.write(name)
    g.write(';'+str(nb_columns))
    g.write(';'+str(true_nb_columns))
    for k in range(1,6):
        g.write(';' + str(rms(np.array(felt_kps),k)))
        g.write(';' + str(rms(np.array(kps),k)))
    g.write('\n')

g.close()
