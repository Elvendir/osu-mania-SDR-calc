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


g = codecs.open('DATAs','w','utf-8')
print('Folder with only .osu files')
folder_path = input()

songs_new_difficulty = []

for element in os.listdir(folder_path):

	file_path = folder_path+element

	(osu_difficulty,map,nb_columns)=extract_info(file_path)
	
	(stamina,kps_columns,i_columns) = calc_stamina(map,nb_columns)
	
	kps=calc_kps(kps_columns,i_columns,map)
	overall_difficulty = calc_overall_difficulty(np.array(stamina),np.array(kps))
	g.write(name';'overall_difficulty)
	songs_new_difficulty.append(overall_difficulty)

g.close()




