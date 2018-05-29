import numpy as np
import matplotlib.pyplot as plt


def plot_kps_felt_kps_graphics(name, nb_columns, i_columns, kps_columns, felt_kps, t):
    plt.figure()
    plt.title(name)
    for k in range(nb_columns):
        i = len(felt_kps) - 1
        if i_columns[i - 1][k] != i:
            i = i_columns[i - 1][k]
        t_k = [t[i]]
        felt_kps_k = [felt_kps[i]]
        kps_k = [kps_columns[i][k]]
        while i_columns[i - 1][k] > 0:
            i = i_columns[i - 1][k]
            t_k.append(t[i])
            felt_kps_k.append(felt_kps[i])
            kps_k.append(kps_columns[i][k])
        plt.subplot(nb_columns, 1, k + 1)
        plt.plot(t_k, (np.array(felt_kps_k)**2-np.array(kps_k)**2), 'b', linewidth=0.5)

