import numpy as np

power_kps = 2  # overall_difficulty power dependency on kps
LN_release_kps_correction = 70  # kps correction for LN release
LN_note_after_release_correction = 150  # kps correction for note after LN release

kps_cap = 50 #cap kps by fixing minimal amount between two notes for trill kps calculation

main_trill_coef = 1.4
border_trill_coef_bot = 0.8
border_trill_coef_top = 1.


def delete_LN_release(map):
    k=0
    i=0
    n = len(map)
    while i+k<n:
        if map[i][1] == 2:
            map = np.delete(map, i, 0)
            k+=1
        else :
            i+=1
    return(map)


def rms(list, k):  # gives the root mean square of a np.array
    return pow(np.mean(list ** k), 1 / k)


def trill_kps_calc(t,d,kps0,kps2, cut_point):
    kpsB = border_trill_coef_top*kps0
    kpsA = border_trill_coef_bot*kps2
    if t/d > cut_point :

        return(  2*(1-main_trill_coef)*(1-t/d)*kpsB + kpsB  )
    else :
        nice = 2*(1-main_trill_coef)*kpsB*(1-cut_point) + kpsB
        return(kpsA +  t/d/cut_point * (nice-kpsA))

def last_trill_kps_calc(t,kps2,cut_point):
    kpsA = border_trill_coef_bot*kps2
    return max(0,kpsA *(1 - t/cut_point ) )


def next_kps(last_i,map):
    column = map[:,0]
    t = map[:,2]
    t1t2 = t[last_i[1]]-t[last_i[2]]
    t0t2 = t[last_i[0]]-t[last_i[2]]
    t2t3 = max(kps_cap,t[last_i[2]]-t[last_i[3]])
    cut_point = min(0.5, t2t3/t0t2)

    if column[last_i[1]] == column[last_i[2]]:
        kps = 1000/t1t2
    elif t1t2 == 0 :
        kps = 1000/t2t3
    elif t2t3 == 0 :
        kps = 1000/t1t2
    else :
        kps = trill_kps_calc(t1t2,t0t2,1000/t0t2,1000/t2t3,cut_point)
    return(kps)

def last_kps(last_i,map):
    column = map[:,0]
    t = map[:,2]
    t0t1 = t[last_i[0]]-t[last_i[1]]
    t1t2 = t[last_i[1]]-t[last_i[2]]

    if column[last_i[0]] == column[last_i[1]]:
        kps = 1000/t0t1
    elif t1t2 == 0 :
        kps = 1000/t0t1
    else :
        kps = last_trill_kps_calc(t0t1,1000/t1t2, t1t2)

    return(kps)


def calc_kps(map,nb_columns):
    columns = map[:, 0]
    kps = [0 for i in range(len(map))]
    last_left_i=[-1,-1,-1,-1]
    count_l =0
    last_right_i=[-1,-1,-1,-1]
    count_r = 0

    for i in range(0, len(map)):
        column = columns[i]
        if column < nb_columns/2 :
            last_left_i[3] = last_left_i[2]
            last_left_i[2] = last_left_i[1]
            last_left_i[1] = last_left_i[0]
            last_left_i[0] = i
            count_l += 1
            if count_l >= 3:
                kps[last_left_i[1]] = next_kps(last_left_i,map)


        else :
            last_right_i[3] = last_right_i[2]
            last_right_i[2] = last_right_i[1]
            last_right_i[1] = last_right_i[0]
            last_right_i[0] = i
            count_r += 1
            if count_r >= 3:
                kps[last_right_i[1]] = next_kps(last_right_i,map)

    kps[last_right_i[0]] = last_kps(last_left_i, map)
    kps[last_right_i[0]] = last_kps(last_right_i, map)

    return kps




def calc_overall_difficulty(individual_difficulty, kps):  # root mean square of ind_difficulty*kps^2
    return rms(individual_difficulty * kps ** power_kps)
