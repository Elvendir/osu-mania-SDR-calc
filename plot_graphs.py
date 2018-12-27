import numpy as np
import matplotlib.pyplot as plt


def plot_kps_felt_kps_graphics(name, left_i ,right_i , kps, felt_kps, t):
    plt.figure()
    plt.title(name)
    t_k = []
    felt_kps_k = []
    kps_k =[]
    for i in range(len(left_i)):
        t_k.append(t[left_i[i]])
        kps_k.append(kps[left_i[i]])
        felt_kps_k.append(felt_kps[left_i[i]])
        plt.subplot(2, 1, 1)
        plt.plot(t_k, (np.array(felt_kps_k)-np.array(kps_k)), 'b', linewidth=0.5)
    t_k = []
    felt_kps_k = []
    kps_k = []
    for i in range(len(right_i)):
        t_k.append(t[right_i[i]])
        kps_k.append(kps[right_i[i]])
        felt_kps_k.append(felt_kps[right_i[i]])
        plt.subplot(2, 1, 2)
        plt.plot(t_k, (np.array(felt_kps_k) - np.array(kps_k)), 'b', linewidth=0.5)

