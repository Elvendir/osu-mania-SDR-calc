import numpy as np
import matplotlib.pyplot as plt
from calc_stamina import G as func_G
from calc_kps import calc_trill_kps as trill


def tab_k(tab, list_i):
    tab_k = []
    for i in range(len(list_i)):
        tab_k.append(tab[list_i[i]])
    return (tab_k)


def kps_VS_complexity(kps, complexity, name):
    plt.figure()
    plt.title("kps VS complexity")
    (m, b) = np.polyfit(kps, complexity, 1)
    fit_fn = np.poly1d(np.array([m, b]))
    plt.plot(kps, complexity, '.')
    plt.plot(kps, fit_fn(kps))
    plt.savefig("graphs/" + "kps_VS_complexity" + "/" + name + ".png")
    plt.close()


def kps_VS_kps_felt(kps, kps_felt, name):
    plt.figure()
    plt.title("kps VS kps_felt ")
    fit_fn = np.poly1d(np.array([1, 0]))
    plt.plot(kps, kps_felt, '.')
    plt.plot(kps, fit_fn(kps))
    plt.savefig("graphs/" + "kps_VS_kps_felt" + "/" + name + ".png")
    plt.close()


def kps_felt_minus_kps(left_i, right_i, kps, felt_kps, t, name):
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
    plt.savefig("graphs/" + "kps_felt_minus_kps" + "/" + name + ".png")
    plt.close()


def complexity(t, complexity, name):
    plt.figure()
    plt.title("complexity")
    plt.plot(t, complexity)
    plt.savefig("graphs/" + "complexity_t" + "/" + name + ".png")
    plt.close()


def kps(t, complexity , name):
    plt.figure()
    plt.title("kps")
    plt.plot(t, complexity, '.')
    plt.savefig("graphs/" + "kps_t" + "/" + name + ".png")
    plt.close()


def accuracy(data):
    plt.figure(figsize=(20, 10))
    plt.title(" 'accuracy' VS player_level")
    for c, (difficulty, name) in enumerate(data):
        k = c // 10
        tab = ['-', '--', '-.', ':']
        plt.plot(np.linspace(0, len(difficulty) * 0.001, len(difficulty)), difficulty, label=name, linestyle=tab[k])
    plt.legend()
    plt.savefig("graphs/+ Accuracy.png")
    plt.show()


def histogram(data, type, name):
    plt.figure()
    plt.title("Histogram of " + type)
    plt.hist(data, bins=20)
    plt.savefig("graphs/" + type + "/" + name + ".png")
    plt.close()


def G():
    plt.figure()
    plt.title("G ideal reward for stamina")
    t = np.linspace(0, 60, 2000)
    for k in range(10):
        plt.plot(t, func_G(k, t))


def F():
    plt.figure()
    plt.title("F depending on placement of the note inside the trill "
              "\n with kps_previous = 20 kps_trill = 5 to 20 in a 10'01'10'01 pattern")
    for j in np.linspace(0.025, 0.2, 20):
        f = []
        t = np.linspace(0, j, 10000)
        for i in t:
            f.append(trill(j, i, 0.05, True))
        plt.plot(t, f)
