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
 c_1 = border_trill_coef_bot
 c_2 = border_trill_coef_top
 c_3 = main_trill_coef
 F = trill_kps_calc  is two half linear function with the the previous conditions.

(To see a visualisation of F uncomment in main.py the graph section)
 '''

LN_release_kps_correction = 70  # kps correction for LN release
LN_note_after_release_correction = 150  # kps correction for note after LN release

kps_cap = 50  # cap kps by fixing minimal amount time between two notes before the half trill

main_trill_coef = 1.4
border_trill_coef_bot = 0.5
border_trill_coef_top = 1.


# Calculates the kps of the last note of an half trill (it's F)
# Currently it's only two half linear function with intro's conditions respected
def trill_kps_calc(t, d, kps0, kps2, cut_point):
    kpsB = border_trill_coef_top * kps0
    kpsA = border_trill_coef_bot * kps2
    if t / d > cut_point:

        return 2 * (1 - main_trill_coef) * (- 1 + t / d) * kpsB + kpsB
    else:
        nice = 2 * (1 - main_trill_coef) * kpsB * (- 1 + cut_point) + kpsB
        return kpsA + t / d / cut_point * (nice - kpsA)


# Same as previous one but for the last note (because there is not a next_note)
def last_trill_kps_calc(t, kps2, cut_point):
    kpsA = border_trill_coef_bot * kps2
    return max(0, kpsA * (- 1 + t / cut_point))


# Does the kps calculation for a note depending on jack or half trill
def next_kps(i, count, map):
    column = map[:, 0]
    t = map[:, 2]
    t1t2 = t[i[count - 2]] - t[i[count - 3]]
    t0t2 = t[i[count - 1]] - t[i[count - 3]]

    # special case : first calculate note
    if count == 3:
        cut_point = 0.5
        t2t3 = 99999999999
    else:
        t2t3 = max(kps_cap, t[i[count - 3]] - t[i[count - 4]])
        cut_point = min(0.5, t2t3 / t0t2)

    # if jack
    if column[i[count - 2]] == column[i[count - 3]]:
        kps = 1000 / t1t2

    # if same timing than previous note
    elif t1t2 == 0:
        kps = 1000 / t2t3

    # if previous note has same timing than the previous previous one
    elif t2t3 == 0:
        kps = 1000 / t1t2

    # other cases
    else:
        kps = trill_kps_calc(t1t2, t0t2, 1000 / t0t2, 1000 / t2t3, cut_point)
    return (kps)


# Same as previous one but for the last note (because there is not a next_note)
def last_kps(i, count, map):
    column = map[:, 0]
    t = map[:, 2]
    t0t1 = t[i[count - 1]] - t[i[count - 2]]
    t1t2 = t[i[count - 2]] - t[i[count - 3]]

    if column[i[count - 1]] == column[i[count - 2]]:
        kps = 1000 / t0t1
    elif t1t2 == 0:
        kps = 1000 / t0t1
    else:
        kps = last_trill_kps_calc(t0t1, 1000 / t1t2, t1t2)

    return (kps)


# Does the kps calculation for both hand independently
def calc_kps(map, nb_columns):
    columns = map[:, 0]
    kps = [0 for i in range(len(map))]
    left_i = []
    count_l = 0
    right_i = []
    count_r = 0

    for i in range(0, len(map)):
        column = columns[i]

        # left hand calculation
        if column < nb_columns / 2:
            left_i.append(i)
            count_l += 1
            if count_l >= 3:
                kps[left_i[count_l - 2]] = next_kps(left_i, count_l, map)

        # right hand calculation
        else:
            right_i.append(i)
            count_r += 1
            if count_r >= 3:
                kps[right_i[count_r - 2]] = next_kps(right_i, count_r, map)

    # last note calculation
    if count_l > 3:
        kps[left_i[count_l - 1]] = last_kps(left_i, count_l, map)
    if count_r > 3:
        kps[right_i[count_r - 1]] = last_kps(right_i, count_r, map)

    return (kps, left_i, right_i)
