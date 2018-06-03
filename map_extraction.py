import numpy as np
import os
import sys
import codecs
import glob

'''
Extracting all info from .osu file
Structure of map :: list of [column_id, type_note, timing_point]

column_id ordered by left to right from 0 to nb_column
type_note == 0 normal, 1 LN hold, 2 LN release

timing_point are in ms there !!!
'''


def extract_info(file_path):
    file = os.path.abspath(file_path)
    f = codecs.open(file, 'r', 'utf-8')
    rd = f.readline()
    b1 = False
    map = []
    columns = []
    while rd:
        b2 = False
        if b1:
            object = rd.split(',')
            for column in columns:
                if column == int(object[0]):  # detecting new columns
                    b2 = True
            if not b2:
                columns.append(int(object[0]))
            if object[3] == '128':  # detecting LNs
                map.append((int(object[0]), 1, int(object[2])))
                time = object[5].split(':')[0]
                map.append((int(object[0]), 2, int(time)))
            else:
                map.append((int(object[0]), 0, int(object[2])))
        if rd.count('HitObjects') == 1:  # searching first note
            b1 = True
        if rd.count('CircleSize') == 1:  # searching first note
            true_nb_column = int(rd.split(':')[1])
        rd = f.readline()
    columns.sort()
    for k in range(len(map)):  # rewriting column_id
        i = 0
        for column in columns:
            if column == map[k][0]:
                map[k] = (i, map[k][1], map[k][2])
            i += 1
    f.close()
    dtype = [('column', int), ('type', int), ('timing', int)]
    map = np.array(map, dtype=dtype)
    map = np.sort(map, order='timing', kind='mergesort')
    map_array = []
    for i in range(len(map)):
        map_array.append([map[i][0], map[i][1], map[i][2]])
    map_array = np.array(map_array)
    return (map_array, len(columns), true_nb_column)
