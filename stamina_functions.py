import numpy as np

kps_target = 5
tau_target = 60
tau_kps_mean = 10
tau_higher = 30
tau_lower = 1
tau_s_memory = 20
LN_release_kps_correction = .05
LN_note_after_release_correction = .1

def increment_i_column(i,i_columns,column) :
	current_i_columns = [i_columns[i-1][k] for k in range(len(i_columns[i-1]))]
	current_i_columns[column] = i
	return(np.array(current_i_columns))

def next_kps(i,i_columns,t,column,kps_columns,type) :
	kps = [kps_columns[i-1][k] for k in range(len(kps_columns[i-1]))]
	if i_columns[i-1][column] != -1 :
		if type[i] == 2 :
			Delta_t = t[i] - t[i_columns[i-1][column]] + LN_release_kps_correction
			kps[column] =  1 / Delta_t
		if type[i_columns[i-1][column]] == 2 :
			Delta_t = max((t[i] - t[i_columns[i-1][column]] + LN_release_kps_correction, t[i] - t[i_columns[i_columns[i-1]][column]]))
			kps[column] =  1 / Delta_t
		else :
			Delta_t = t[i] - t[i_columns[i-1][column]] 
			kps[column] =  1 / Delta_t
	return(np.array(kps))

def G(kps,t) :
	return 0.5*(pow(t/tau_target+1,kps**2/kps_target**2+1)-(t/tau_target+1))

def d_G(kps,t) :
	return (kps**2/kps_target**2+1)*(0.5/tau_target)*pow(t/tau_target+1,kps**2/kps_target**2)-0.5/tau_target

def calc_target(kps,t,s,list_i,i) :

	j = i
	j_p1 = j
	j_max = 0
	kps_min = kps[i]
	s_targeted = 0
	s_targeted_max = 0
	dg = 0
	dg_max = 0
	kps_mean = kps[i]

	while list_i[j-1] > 0 :
		Delta_t = t[j]-t[list_i[j-1]]
		kps_mean = kps_mean + (kps[j] - kps_mean)*Delta_t/tau_kps_mean
		if kps_mean <= kps_min :
			kps_min = kps_mean
		j_p1 = j
		j = list_i[j-1]
		s_targeted = G(kps_min,t[i]-t[j]) 
		if s_targeted >= s_targeted_max :
			s_targeted_max = s_targeted
			j_max = j
		dg = d_G(kps_min,t[i]-t[j])
		if dg > dg_max :
			dg_max = dg
	
	return (s_targeted_max,dg_max)


def dif_eq(kps,t,s,list_i,i):
	i_m1 = list_i[i-1]
	Delta_t = t[i]-t[i_m1]
	(s_targeted, dg) = calc_target(kps,t,s,list_i,i)
	if s[i_m1] > s_targeted :
		return s[i_m1] + dg*Delta_t + (s_targeted - s[i_m1])*Delta_t/tau_higher
	else:
		return s[i_m1] + dg*Delta_t + (s_targeted - s[i_m1])*Delta_t/tau_lower 