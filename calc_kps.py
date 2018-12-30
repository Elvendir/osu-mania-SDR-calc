import numpy as np
import matplotlib.pyplot as plt

'''
The aim is to give each note an individual kps.
First, kps is calculate for each hand independently .
(because for a player kps is linked to the frequency of the hand not to the fingers's one).

For a jack it's simple : kps = 1/time_btw_the_2_notes

However, when there is a trill or two notes at the same time it gets more complicated.
First, two notes at the same time can be seen as the limit of an half trill (two notes not on the same column)
 when the two notes are infinitely near of each other.

By using this principle, kps of a note at the end of the half trill is calculate by :
 kps = F(kps_previous_note, delta_t_previous_note|note, delta_t_note|next_note)

And the limit implies : F(kps,0,t)= kps * c_1 and F(kps,t,0) = c_2 / delta_t_note|next_note
 with c_1 and c_2 constant <= 1 that decrease the reward for two note pressed at the same time.

The other interesting value is : F(kps,t,t) = c_3 / (2*t) when there is a perfect trill
 (the note is exactly in the middle of the two others)
 with c_3 a constant >= 1 that rewards the trill.

In the calculation :
 c_1 = 1 (because at least one of a double need to have a full_weight)
 c_2 = mash_coef(kps_previous)
 c_3 = trill_coef
 F = trill_kps_calc  is two half linear function with the the previous conditions.

(To see a visualisation of F uncomment in main.py the graph section)
 '''

LN_release_kps_correction = 70  # kps correction for LN release
LN_note_after_release_correction = 150  # kps correction for note after LN release

tau_mash = 0.1  # size in seconds of the mash zone

trill_coef = 0.7  # factor of reduction of the trill kps
tau_kps_trill = 2  # typical kps at which the kps of the previous is taken into account

kps_ez = 6  # kps at which it's sure to have both note of a jump jack
kps_hard = 12  # kps at which it's impossible to have both note of a jump jack


# useful functions to calculated trill_kps
def something(x):
    return (np.cos(x * np.pi / 2)) ** 2


def quarter_ellipse(t, top, bottom):
    m = top - bottom
    if t >= tau_mash:
        return top
    elif t <= 0:
        return bottom
    else:
        return -m * np.sqrt(1 - (t / tau_mash) ** 2) + top


# definition of the variables coefficient
def mash_coef(kps_previous):
    if kps_previous < kps_ez:
        return 0
    elif kps_previous > kps_hard:
        return 1
    else:
        return something(kps_previous / (kps_hard - kps_previous))


def variable_trill_coef(kps):
    if kps == 0:
        return trill_coef
    else:
        return trill_coef - np.exp(-tau_kps_trill / kps) * (trill_coef - 1)


# Calculates the note's kps has a trill
def calc_trill_kps_has_trill(t1t2, t0t2, p):
    return p * (1 / t1t2 - 1 / t0t2) + 1 / t0t2


# Calculates the note's kps when it can be smashed
def calc_trill_kps_has_mash(t1t2, max_trill_kps, previous_kps):
    return quarter_ellipse(t1t2, max_trill_kps, previous_kps * mash_coef(previous_kps))


# Calculates the kps of the last note of an half trill (it's F)
# It's two half function : one for the trill part the other for the mashing (when near the previous note)
def trill_kps_calc(t0t2, t1t2, t2t3, jack_limit):
    kps_previous = 1 / t2t3

    # If column1 == column3 then at the limit when t2t3 = 0 it becomes a jack
    if not jack_limit:
        p = 2 * variable_trill_coef(0) - 1
    else:
        p = 2 * variable_trill_coef(kps_previous) - 1

    trill_kps_has_trill = calc_trill_kps_has_trill(t1t2, t0t2, p)

    # Distinguish between mash and trill zone
    if t1t2 < tau_mash:
        trill_kps_has_mash = calc_trill_kps_has_mash(t1t2, calc_trill_kps_has_trill(tau_mash, t0t2, p),
                                                     kps_previous * mash_coef(kps_previous))
        return min(trill_kps_has_mash, trill_kps_has_trill)
    else:
        return trill_kps_has_trill


# Does the kps calculation for a note depending on jack or half trill
def next_kps(i, count, map, last_LN_start, last):
    column = map[:, 0]
    type = map[:, 0]
    t = map[:, 2] / 1000

    t1t2 = t[i[count - 2]] - t[i[count - 3]]

    # if jack
    if column[i[count - 2]] == column[i[count - 3]]:
        kps = 1 / t1t2
        return kps

    # special case : first calculate note
    # jack limit is a bool saying if when t2t3 = 0 the note is a jack
    if count == 3:
        t2t3 = float("inf")
        jack_limit = False
    else:
        t2t3 = t[i[count - 3]] - t[i[count - 4]]
        jack_limit = (column[i[count - 2]] == column[i[count - 4]])

    # special case : last calculate note
    if last:
        t0t2 = float("inf")
    else:
        t0t2 = t[i[count - 1]] - t[i[count - 3]]

    kps = trill_kps_calc(t0t2, t1t2, t2t3, jack_limit)
    return kps


# Does the kps calculation for both hand independently
def calc_kps(map, nb_columns):
    columns = map[:, 0]
    type = map[:, 1]
    kps = [0 for i in range(len(map))]
    last_LN_start = [-1 for i in range(nb_columns)]
    left_i = []
    count_l = 0
    right_i = []
    count_r = 0
    last = False

    for i in range(0, len(map)):
        column = columns[i]
        if type[i] == 1:
            last_LN_start[column] = i

        # left hand calculation
        if column < nb_columns / 2:
            left_i.append(i)
            count_l += 1
            if count_l >= 3:
                kps[left_i[count_l - 2]] = next_kps(left_i, count_l, map, last_LN_start, last)

        # right hand calculation
        else:
            right_i.append(i)
            count_r += 1
            if count_r >= 3:
                kps[right_i[count_r - 2]] = next_kps(right_i, count_r, map, last_LN_start, last)

    # last note calculation
    count_l += 1
    count_r += 1
    last = True
    if count_l > 3:
        kps[left_i[count_l - 2]] = next_kps(left_i, count_l, map, last_LN_start, last)
    if count_r > 3:
        kps[right_i[count_r - 2]] = next_kps(right_i, count_r, map, last_LN_start, last)

    return kps, left_i, right_i
