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

(To see a visualisation of F uncomment in main.py the graph section or try https://www.desmos.com/calculator/8pdbpj1u59)
 '''

LN_release_kps_correction = 70  # kps correction for LN release
LN_note_after_release_correction = 150  # kps correction for note after LN release

t_mash_min = 0.1  # size in seconds of the mash zone

trill_coef = 0.7  # factor of reduction of the trill kps
tau_kps_trill = 2  # typical kps at which the kps of the previous is taken into account

kps_ez = -1  # kps at which it's sure to have both note of a jump jack
kps_hard = 0  # kps at which it's impossible to have both note of a jump jack

tau_jack = 10  # time between two note when you can't start to jack and the next
tau_kps_jack = 10  # typical kps at which it stats to take into account the previous one


# useful functions to calculated trill_kps
def something(x):
    return (np.cos(x * np.pi / 2)) ** 2


def hyperbole(x, hyperbole_slope, y):
    return x / 2 / hyperbole_slope - np.sqrt((x / 2 / hyperbole_slope) ** 2 + y)


def calc_hyperbole_slope(t_mash, kps_previous, kps_trill):
    m = kps_previous - (1 / t_mash) ** 2
    T = 0.5 * ((trill_coef / t_mash - kps_trill) / (1 / t_mash - kps_trill) + 1)
    ln_thing = (trill_coef - T) / (trill_coef - 1)
    if ln_thing <= 0:
        return 0
    else:
        Q = kps_previous * np.log(ln_thing)
        return (1 / Q) * hyperbole(m, 1, kps_previous)


def quarter_ellipse(t, max_trill_kps, mash_kps, t_mash):
    if t >= t_mash:
        return max_trill_kps
    elif t <= 0:
        return mash_kps
    else:
        return (mash_kps - max_trill_kps) * np.sqrt(1 - (t / t_mash) ** 2) + max_trill_kps


# definition of the variables coefficient
def calc_mash_kps(t1t2, t2t3):
    kps_previous = 1 / t2t3

    if t1t2 == 0:
        if kps_previous == 0:
            mash_kps = 0
        else:
            mash_kps = kps_previous
    elif kps_previous == 0:
        mash_kps = 0

    else:
        mash_kps = kps_previous

    if mash_kps <= kps_ez:
        return 0
    elif kps_previous >= kps_hard:
        return mash_kps
    else:
        return something(mash_kps / (kps_hard - kps_ez))


# Defines the change in trill_coef when it becomes a jack (limit t1t2 = 0)
def jack_limit_coef(t0t2, t1t2, t2t3, t_mash):
    kps_previous = 1 / t2t3
    hyperbole_slope = calc_hyperbole_slope(t_mash, kps_previous, 1 / t0t2)
    if hyperbole_slope == 0:
        return 0
    q = hyperbole(kps_previous - (1 / t1t2) ** 2, hyperbole_slope, kps_previous)
    return np.exp(q / kps_previous)


# Defines a variable trill_coef to take into account the fact that it can become a jack
# at the limit t2t3 = 0
def variable_trill_coef(t0t2, t1t2, t2t3, jack_limit, t_mash):
    kps_previous = 1 / t2t3

    if kps_previous == 0:
        return trill_coef
    elif t1t2 == 0:
        return 1
    elif not jack_limit:
        return trill_coef
    else:
        return trill_coef - jack_limit_coef(t0t2, t1t2, t2t3, t_mash) * (trill_coef - 1)


# Calculates the note's kps has a trill
def calc_trill_kps_has_trill(t1t2, t0t2, m_trill_coef):
    return (2 * m_trill_coef - 1) * (1 / t1t2 - 1 / t0t2) + 1 / t0t2


# Calculates the note's kps when it can be smashed
def calc_trill_kps_has_mash(t1t2, max_trill_kps, mash_kps, t_mash):
    return quarter_ellipse(t1t2, max_trill_kps, mash_kps, t_mash)


# Calculates the kps of the last note of an half trill (it's F)
# It's two half function : one for the trill part the other for the mashing (when near the previous note)
def trill_kps_calc(t0t2, t1t2, t2t3, jack_limit):
    t_mash = min([t_mash_min, t0t2 / 2, t2t3])

    m_trill_coef = variable_trill_coef(t0t2, t1t2, t2t3, jack_limit, t_mash)

    trill_kps_has_trill = calc_trill_kps_has_trill(t1t2, t0t2, m_trill_coef)

    # Distinguish between mash and trill zone
    if t1t2 < t_mash:
        trill_kps_has_mash = calc_trill_kps_has_mash(t1t2, calc_trill_kps_has_trill(t_mash, t0t2, m_trill_coef),
                                                     calc_mash_kps(t1t2, t2t3), t_mash)
        return min(trill_kps_has_mash, trill_kps_has_trill)
    else:
        return trill_kps_has_trill


# Does the kps calculation for a note depending on jack or half trill
def next_kps(i, count, map, last_LN_start, last):
    column = map[:, 0]
    type = map[:, 0]
    t = map[:, 2] / 1000

    t1t2 = t[i[count - 2]] - t[i[count - 3]]

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

    # if jack
    if column[i[count - 2]] == column[i[count - 3]]:
        return 1 / t1t2
    if t2t3 == 0:
        return 1 / t1t2
    if t0t2 - t1t2 == 0:
        return 1 / t1t2
    if t1t2 == 0:
        return 1 / t2t3

    # if jack but the other way around

    else:
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
