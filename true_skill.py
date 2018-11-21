# -*- coding: utf-8 -*-
from trueskill import Rating, rate_1vs1
import numpy as np
import os
import operator

def _print_rate(rate_list):
	print('current rate:', [rate_list[ii] for ii in rate_list], '\n')

def extract_idx(file_name):
	name_list = file_name.split('_')
	return int(name_list[3])
	 
rate_list = {i: Rating() for i in range(1,5)} # 给出一个字典

#update
#play_result = [[1, 0, 0], [1, 2, -1]]
path = 'result/'
for ff in os.listdir(path):
	if  '.txt' not in ff:
		continue
	# play_result = np.loadtxt(path + ff)
	play_result = open(path+ff)
 	for ii in play_result:
		ii = ii.strip().split(' ')
		idx1 = extract_idx(ii[2])
		idx2 = extract_idx(ii[3])
		if ii[4] == '-1':
			new_1, new_2 = rate_1vs1(rate_list[idx1], rate_list[idx2], drawn=True)
			rate_list[idx1], rate_list[idx2] = new_1, new_2
		elif ii[4] == '0':
			new_1, new_2 = rate_1vs1(rate_list[idx1], rate_list[idx2])
			rate_list[idx1], rate_list[idx2] = new_1, new_2
			
		elif ii[4] == '1':
			new_1, new_2 = rate_1vs1(rate_list[idx2], rate_list[idx1])
			rate_list[idx2], rate_list[idx1] = new_1, new_2

		# _print_rate(rate_list)
rate_list = sorted(rate_list.items(), lambda x, y: cmp(x[1].mu, y[1].mu), reverse=True)
mu_sig = ['{} {} {}\n'.format(ii[0], ii[1].mu, ii[1].sigma) for ii in rate_list]
with open('mu_sig.txt', 'w') as f:
	f.writelines(mu_sig)
