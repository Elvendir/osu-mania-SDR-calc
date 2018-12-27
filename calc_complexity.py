import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt

'''
Reminder : type_note == 0 normal, 1 LN hold, 2 LN release
'''

TF_time_scale = 1
sample_size = 2000

def create_array(map,nb_columns):
    sample = []
    t = map[:,2]
    column = map[:,0]
    for i in range(sample_size):
        sample.append(np.array([0 for k in range(nb_columns+50*(nb_columns-1))]))
    i=0
    j=0
    tc = t[0] + j * TF_time_scale
    while t[i] <= tc :
        sample[j][column[i]*50] = 1
        i += 1
    j = 1
    return(sample,j,i)



def increment_array(sample,j,i, map, nb_columns ):
    sample.pop(0)
    t = map[:,2]
    column = map[:,0]
    sample.append(np.array([0 for k in range(nb_columns + 50 * (nb_columns - 1))]))
    tc = t[0] + j * TF_time_scale
    while  i < len(map) and t[i] <= tc :
        sample[sample_size-1][column[i]*50] = 1
        i +=1
    j += 1
    return(sample,j,i)



def calc_complexity(map, nb_columns):
    (sample,j,i) = create_array(map, nb_columns)
    a_sample = np.array(sample)

    t = map[:,0]
    while tc < t[len(t)-1]+TF_time_scale*sample_size :
        a_sample = np.array(sample)
        fft_sample = abs(np.fft.rfft2(a_sample))
        cmap = plt.get_cmap('PiYG')
        if j%1000 == 0 :
            plt.pcolormesh(fft_sample)
            plt.show()
        (sample,j,i)=increment_array(sample,j,i,map,nb_columns)
        tc = t[0] + j * TF_time_scale
