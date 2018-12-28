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

import lot_of_graphs as graph


'''
Calculates difficulty for each .osu file in folder_path.
Writes all lot of things in a DATA file.

I'm trying to keep this as much commented as possible.
Information on each calculation can be found in their respective files.

How this works :
- calculates an individual kps
- corrects it into a felt_kps by taking stamina into account
- multiplies kps_felt by a individual complexity 
- takes the mean 

At the end of this file, you can find a lot of graphs to plot by uncommenting.


TO DO :
- Take into account LNs
- Make a more precise calc_complexity
- Tweak overall_difficulty calculation (change the multiply between complexity and kps_felt)
- Generalise to N Keys style
- Tweak all constant (for stamina, complexity, kps)
- Probably others things
...
- Do a progressive calculation (make difficulty depends on player' s level)
'''

g = codecs.open('DATAs', 'w', 'utf-8')
g.write('name;nb_column;true_nb_columns;calc_time;kps;felt_kps;complexity;overall_dif \n')

print('Path of folder with only .osu files')
folder_path = input()

# Calculates the difficulties for each map
for element in os.listdir(folder_path):
    t0 = time.time()
    file_path = folder_path + '/' + element
    name = element

    (map, nb_columns, true_nb_columns) = extract_info(file_path)
    map = delete_LN_release(map)  # Deletes LN's release because not implemented yet

    (kps, left_i, right_i) = calc_kps(map, nb_columns)

    felt_kps = [0 for i in range(len(map))]

    felt_kps = calc_felt_kps(map, left_i, kps, felt_kps, 0)
    felt_kps = calc_felt_kps(map, right_i, kps, felt_kps, len(left_i))

    complexity = calc_complexity(map, nb_columns)

    mean_kps = np.mean(np.array(kps))
    mean_felt_kps = np.mean(np.array(felt_kps))
    mean_complexity = np.mean(np.array(complexity))

    # Current calculation of overall_difficulties is a multiplication
    overall_difficulty = np.mean(np.array(complexity) * np.array(felt_kps))

    # Writes information into the file
    # (if there is a difference between nb_columns and true_nb_columns the map isn't well encoded)
    g.write(name)
    g.write(';' + str(nb_columns))
    g.write(';' + str(true_nb_columns))
    g.write(';' + str((time.time() - t0)))
    g.write(';' + str(mean_kps))
    g.write(';' + str(mean_felt_kps))
    g.write(';' + str(mean_complexity))
    g.write(';' + str(overall_difficulty) + '\n')
    sys.stdout.write("\r")

    # Writes information in the terminal
    print('dif = ' + str("%.2f" % overall_difficulty)
          + '; m_c =' + str("%.2f" % mean_complexity)
          + '; m_f_kps = ' + str("%.2f" % mean_felt_kps)
          + '; m_kps = ' + str("%.2f" % mean_kps)
          + '; calc_t = ' + str("%.2f" % (time.time() - t0))
          + '; name = ' + name
          + '; nb_note = ' + str(len(map))
          + '; nb_columns = ' + str(nb_columns)
          + '; true_nb =' + str(true_nb_columns))
    sys.stdout.flush()

    '''
    Here is the graph section. 
    Uncomment the graphs that sounds cool or useful (delete the # symbol).
    
    WARNING : 
    It will plot one/multiples graph for each map
    You will need to close them all before it calculates the next map.
    Some graphs can be very heavy.
    
    (For FFT graphs see the calc_complexity.py file)
    '''
    #graph.complexity(map[:, 2], complexity)
    #graph.kps_felt_minus_kps(left_i, right_i, kps, felt_kps, map[:, 2])
    #graph.kps_VS_complexity(kps, complexity)
    #graph.kps_VS_kps_felt(kps, felt_kps)
    #graph.G()
    graph.F()

    plt.show()

g.close()
