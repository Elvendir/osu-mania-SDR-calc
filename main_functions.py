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


def next_kps(i,count,map):

    column = map[:,0]
    t = map[:,2]
    t1t2 = t[i[count-2]]-t[i[count-3]]
    t0t2 = t[i[count-1]]-t[i[count-3]]
    if count == 3 :
        cut_point = 0.5
        t2t3 = 99999999999
    else:
        t2t3 = max(kps_cap, t[i[count - 3]] - t[i[count - 4]])
        cut_point = min(0.5, t2t3 / t0t2)

    if column[i[count-2]] == column[i[count-3]]:
        kps = 1000/t1t2
    elif t1t2 == 0 :
        kps = 1000/t2t3
    elif t2t3 == 0 :
        kps = 1000/t1t2
    else :
        kps = trill_kps_calc(t1t2,t0t2,1000/t0t2,1000/t2t3,cut_point)
    return(kps)

def last_kps(i,count,map):
    column = map[:,0]
    t = map[:,2]
    t0t1 = t[i[count-1]]-t[i[count-2]]
    t1t2 = t[i[count-2]]-t[i[count-3]]

    if column[i[count-1]] == column[i[count-2]]:
        kps = 1000/t0t1
    elif t1t2 == 0 :
        kps = 1000/t0t1
    else :
        kps = last_trill_kps_calc(t0t1,1000/t1t2, t1t2)

    return(kps)


def calc_kps(map,nb_columns):
    columns = map[:, 0]
    kps = [0 for i in range(len(map))]
    left_i=[]
    count_l =0
    right_i=[]
    count_r = 0

    for i in range(0, len(map)):
        column = columns[i]
        if column < nb_columns/2 :
            left_i.append(i)
            count_l += 1
            if count_l >= 3:
                kps[left_i[count_l-2]] = next_kps(left_i,count_l,map)


        else :
            right_i.append(i)
            count_r += 1
            if count_r >= 3:
                kps[right_i[count_r-2]] = next_kps(right_i,count_r,map)

    kps[left_i[count_l-1]] = last_kps(left_i,count_l, map)
    kps[right_i[count_r-1]] = last_kps(right_i,count_r, map)

    return (kps,left_i,right_i)


def calc_overall_difficulty(individual_difficulty, kps):  # root mean square of ind_difficulty*kps^2
    return rms(individual_difficulty * kps ** power_kps)
