import numpy as np
import matplotlib.pyplot as plt
from calc_stamina import G as func_G
from calc_kps import trill_kps_calc as trill


def tab_k(tab, list_i):
    tab_k = []
    for i in range(len(list_i)):
        tab_k.append(tab[list_i[i]])
    return (tab_k)


def kps_VS_complexity(kps, complexity):
    plt.figure()
    plt.title("kps VS complexity")
    (m, b) = np.polyfit(kps, complexity, 1)
    fit_fn = np.poly1d(np.array([m, b]))
    plt.plot(kps, complexity, '.')
    plt.plot(kps, fit_fn(kps))


def kps_VS_kps_felt(kps, kps_felt):
    plt.figure()
    plt.title("kps VS kps_felt ")
    (m, b) = np.polyfit(kps, kps_felt, 1)
    fit_fn = np.poly1d(np.array([m, b]))
    plt.plot(kps, kps_felt, '.')
    plt.plot(kps, fit_fn(kps))


def kps_felt_minus_kps(left_i, right_i, kps, felt_kps, t):
    plt.figure()
    plt.title("kps_felt - kps")

    t_k = tab_k(t, left_i)
    felt_kps_k = tab_k(felt_kps, left_i)
    kps_k = tab_k(kps, left_i)

    plt.subplot(2, 1, 1)
    plt.plot(t_k, (np.array(felt_kps_k) - np.array(kps_k)), 'b.', linewidth=0.5)

    t_k = tab_k(t, right_i)
    felt_kps_k = tab_k(felt_kps, right_i)
    kps_k = tab_k(kps, right_i)
    plt.subplot(2, 1, 2)
    plt.plot(t_k, (np.array(felt_kps_k) - np.array(kps_k)), 'b.', linewidth=0.5)


def complexity(t, complexity):
    plt.figure()
    plt.title("complexity")
    plt.plot(t, complexity)


def G():
    plt.figure()
    plt.title("G ideal reward for stamina")
    t = np.linspace(0, 60, 2000)
    for k in range(10):
        plt.plot(t, func_G(k, t))


def F():
    plt.figure()
    plt.title("F depending on placement of the note inside the trill "
              "\n with kps_previous = kps_next = 1 in a 01'01'10'01 pattern")
    t = np.linspace(0, 1, 10000)
    f = []
    for i in t:
        f.append(trill(1, i, 1, False))
    plt.plot(t, f)
