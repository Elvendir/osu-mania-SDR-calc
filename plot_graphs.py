import numpy as np
import matplotlib.pyplot as plt


def plot_staminas_kps_graphics(name, nb_columns, i_columns, kps_columns, rho, s_local, s_local_max, s_global,
                               s_global_max, t):
    plt.figure()
    for k in range(nb_columns):
        i = len(s_local) - 1
        if i_columns[i - 1][k] != i:
            i = i_columns[i - 1][k]
        t_k = [t[i]]
        s_local_k = [s_local[i]]
        s_local_max_k = [s_local_max[i]]
        kps_k = [kps_columns[i][k]]
        while i_columns[i - 1][k] > 0:
            i = i_columns[i - 1][k]
            t_k.append(t[i])
            s_local_k.append(s_local[i])
            s_local_max_k.append(s_local_max[i])
            kps_k.append(kps_columns[i][k])
        ax1 = plt.subplot(nb_columns + 1, 1, k + 1)
        ax2 = ax1.twinx()
        if k == 0:
            plt.title(name)
        ax2.plot(t_k, kps_k, 'b', linewidth=0.5)
        ax1.plot(t_k, s_local_max_k, 'k', linewidth=1.1)
        ax1.plot(t_k, s_local_k, 'r', linewidth=1)

    ax1 = plt.subplot(nb_columns + 1, 1, nb_columns + 1)
    ax2 = ax1.twinx()
    ax2.plot(t, rho, 'b', linewidth=0.5)
    ax1.plot(t, s_global_max, 'k', linewidth=1.1)
    ax1.plot(t, s_global, 'r', linewidth=1)


def plot_stamina_complexity(stamina, complexity, t):
    plt.figure()
    plt.plot(t, complexity, 'g')
    plt.plot(t, stamina, 'b')
    plt.plot(t, complexity * stamina, 'r')
