import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import codecs
import glob
import time
from main_functions import delete_LN_release
from map_extraction import extract_info
from calc_kps import calc_kps
from calc_stamina import calc_felt_kps
from calc_complexity import calc_complexity

'''
Calculate difficulty for each .osu file in folder_path
Write all song_name;difficulty in a DATA file
'''

g = codecs.open('DATAs', 'w', 'utf-8')
print('Folder with only .osu files')
folder_path = input()
g.write('name;nb_column;true_nb_columns;kps;felt_kps;complexity;m;b;overall_dif \n')

for element in os.listdir(folder_path):


    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element
    (map, nb_columns, true_nb_columns) = extract_info(file_path)
    map=delete_LN_release(map)
    (kps, left_i, right_i) = calc_kps(map, nb_columns)

    felt_kps = [0 for i in range(len(map))]

    felt_kps = calc_felt_kps(map, left_i, kps, felt_kps,0)
    felt_kps = calc_felt_kps(map, right_i, kps, felt_kps, len(left_i))

    complexity = calc_complexity(map, nb_columns)

    mean_kps = np.mean(np.array(kps))
    mean_felt_kps =np.mean(np.array(felt_kps))
    mean_complexity = np.mean(np.array(complexity))

    overall_difficulty = np.mean(np.array(complexity)*np.array(felt_kps))
    (m,b) = np.polyfit(kps, complexity, 1)

    g.write(name)
    g.write(';' + str(nb_columns))
    g.write(';' + str(true_nb_columns))
    g.write(';' + str(mean_kps))
    g.write(';' + str(mean_felt_kps))
    g.write(';' + str(mean_complexity))
    g.write(';' + str(m))
    g.write(';' + str(b))
    g.write(';' + str(overall_difficulty) + '\n' )
    sys.stdout.write("\r")
    print('dif = ' + str("%.2f" % overall_difficulty)
          + '; m_c ='+ str("%.2f" % mean_complexity)
          + '; m =' + str("%.2f" % m)
          + '; b =' + str("%.2f" % b)
          + '; m_f_kps = ' + str("%.2f" % mean_felt_kps)
          + '; m_kps = ' + str("%.2f" % mean_kps)
          + '; calc_t = ' + str("%.2f" % (time.time() - t0))
          + '; name = ' + name
          + '; nb_note = ' + str(len(map))
          + '; nb_columns = ' + str(nb_columns)
          + '; true_nb =' + str(true_nb_columns))
    sys.stdout.flush()

'''
    fit_fn = np.poly1d(np.array([m,b]))
    plt.plot(kps,complexity,'.')
    plt.plot(kps,fit_fn(kps))
    plt.show()
'''

g.close()
