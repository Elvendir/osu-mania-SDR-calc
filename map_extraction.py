import numpy as np
import os
import sys
import codecs
import glob


def extract_info(file):
    file = os.path.abspath(file)
    f = codecs.open(file, 'r', 'utf-8')
    rd = f.readline()
    b1 = False
    map = []
    columns = []
    i = 0
    while rd:
        b2 = False
        if b1:
            object = np.array(rd.split(','))
            for column in columns:
                if column == int(object[0]):
                    b2 = True
            if not (b2):
                columns.append(int(object[0]))
            if object[3] == 128:
                map.append(np.array([int(object[0]), 1, int(object[2])]))
                map.append(np.array([int(object[0]), 2, int(object[5])]))
            else:
                map.append(np.array([int(object[0]), 0, int(object[2])]))
        if rd.count('HitObjects') == 1:
            b1 = True
        rd = f.readline()
    columns.sort()
    for object in map:
        i = 0
        for column in columns:
            if column == object[0]:
                object[0] = i
            i += 1
    f.close()
    map = np.array(map)
    return (map, len(columns))
