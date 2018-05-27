import numpy as np
from stamina_functions import *
from main_functions import * 

def calc_stamina(map,nb_columns) :
	t = map[:,2]/1000
	type = map[:,1]
	s_local = [0]
	s_global = [0]

	i_columns = [np.array([-1 for k in range(nb_columns)])]
	kps_columns = [np.array([0 for k in range(nb_columns)])]
	rho = [0]

	column = map[0][0]
	i_columns[0][column] += 1
	trivial_list = [k for k in range(len(map))]
	
	for i in range (1,len(map)) :
		column = map[i][0]
		i_columns.append(increment_i_column(i,i_columns,column))
		kps_columns.append(next_kps(i,i_columns,t,column,kps_columns,type))	

		if i_columns[i-1][column] == -1 :
			s_local.append(0)
	
		else :
			current_s = dif_eq(np.array(kps_columns)[:,column],t,s_local,np.array(i_columns)[:,column],i)
			s_local.append(current_s)
	
	kps_columns_copy = np.copy(np.array(kps_columns))
	for i in range (len(map)-2,0,-1) :
		if i == len(map)-2 :
			for k in range(nb_columns) :
				if i_columns[i-1][k] == i_columns[i][k] :
					kps_columns_copy[i][k] = 0
		else :
			for k in range(nb_columns) :
				if i_columns[i-1][k] == i_columns[i][k] :
					kps_columns_copy[i][k] = kps_columns_copy[i+1][k]
				
	for i in range (1,len(map)) :				
		rho.append(rms(kps_columns_copy[i]))
		current_s = dif_eq(rho,t,s_global,trivial_list,i)
		s_global.append(current_s)
	
	
	
	
		
	return(1+np.array(s_local)+np.sqrt(nb_columns-1)*np.array(s_global)/4,kps_columns,i_columns)
	
