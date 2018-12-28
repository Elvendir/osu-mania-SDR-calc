import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt

'''
Reminder : type_note == 0 normal, 1 LN hold, 2 LN release
'''

TF_time_scale = 1
sample_size = 2000
note_placement = 999
space_btw_columns = 10

def create_array(map,nb_columns):
    sample = []
    t = map[:,2]
    column = map[:,0]
    for i in range(sample_size):
        sample.append(np.array([0 for k in range(nb_columns+space_btw_columns*(nb_columns-1))]))
    i=0
    j=0
    tc = t[0] + (j+note_placement) * TF_time_scale
    while t[i] <= tc :
        sample[note_placement][column[i]*space_btw_columns] = 1
        i += 1
    j = 1
    return(sample,j,i)



def increment_array(sample,j,i, map, nb_columns ):
    t = map[:,2]
    column = map[:,0]
    nb_note =  0
    tc = t[0] + (j+note_placement) * TF_time_scale
    while t[i] > tc :
        j += 1
        sample.pop(0)
        sample.append(np.array([0 for k in range(nb_columns + space_btw_columns * (nb_columns - 1))]))
        tc += TF_time_scale

    while i < len(map) and t[i] <= tc :
        sample[note_placement][column[i] * space_btw_columns] = 1
        nb_note += 1
        i += 1
    return(sample, j, i, nb_note )



def calc_complexity(map, nb_columns):
    complexity=[]
    t = map[:,2]



    (sample,j,i) = create_array(map, nb_columns)
    a_sample = np.array(sample)
    fft_sample = abs(np.fft.rfft2(a_sample))
    for k in range(i):
        complexity.append(np.sum(fft_sample))

    while i < len(map) :
        (sample,j,i, nb_note)=increment_array(sample,j,i,map,nb_columns)
        a_sample = np.array(sample)
        fft_sample = abs(np.fft.rfft2(a_sample))
        for k in range(nb_note):
            complexity.append(np.sum(fft_sample))
        cmap = plt.get_cmap('PiYG')
        '''
        if j % 10000 == 0 :
            plt.pcolormesh(fft_sample)
            plt.show()
        '''
    return(complexity)
