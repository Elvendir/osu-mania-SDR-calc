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
            object = np.array(rd.split(','))
            for column in columns:
                if column == int(object[0]):  # detecting new columns
                    b2 = True
            if not b2:
                columns.append(int(object[0]))
            if object[3] == 128:  # detecting LNs
                map.append(np.array([int(object[0]), 1, int(object[2])]))
                map.append(np.array([int(object[0]), 2, int(object[5])]))
            else:
                map.append(np.array([int(object[0]), 0, int(object[2])]))
        if rd.count('HitObjects') == 1:  # searching first note
            b1 = True
        rd = f.readline()
    columns.sort()
    for object in map:  # rewriting column_id
        i = 0
        for column in columns:
            if column == object[0]:
                object[0] = i
            i += 1
    f.close()
    map = np.array(map)
    return (map, len(columns))
