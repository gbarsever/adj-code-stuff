#!/usr/bin/python
from __future__ import division

import re
import os
import itertools
from itertools import groupby
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scikits.bootstrap as bootstrap
from scipy.special import comb #comb(N,k, exact=False)

#need for each adj N: numb of adj strings that contained adj, and f the freq adj was in second position



#also p2exp for each hypothesis. export big dictionary and import for calculations (each adj entry will have all numbers needed for each hypothesis, N and f will be same regardless of hypo)

big_adj_dict = {} #N: numb of adj strings that contained adj, and f the freq adj was in second position, frequency, by classes, [by binned], [N: numb of adj strings that contained adj, and f the freq adj was in second position]

log_sum_hyp1 = 0
for adj in big_adj_dict:
    N = big_adj_dict[adj][4]
    f = big_adj_dict[adj][5]
    p2exp = big_adj_dict[adj][0]
    pDadj_H = comb(N, f) * p2exp ^ f * (1 - p2exp) ^ (N - f)
    log_sum += np.log(pDadj_H)

log_sum_hyp2 = 0
for adj in big_adj_dict:
    N = big_adj_dict[adj][4]
    f = big_adj_dict[adj][5]
    p2exp = big_adj_dict[adj][1]
    pDadj_H = comb(N, f) * p2exp ^ f * (1 - p2exp) ^ (N - f)
    log_sum += np.log(pDadj_H)

log_sum_hyp3 = 0
for adj in big_adj_dict:
    N = big_adj_dict[adj][4]
    f = big_adj_dict[adj][5]
    p2exp = big_adj_dict[adj][2]
    pDadj_H = comb(N, f) * p2exp ^ f * (1 - p2exp) ^ (N - f)
    log_sum += np.log(pDadj_H)

log_sum_hyp4 = 0
for adj in big_adj_dict:
    N = big_adj_dict[adj][4]
    f = big_adj_dict[adj][5]
    p2exp = big_adj_dict[adj][3]
    pDadj_H = comb(N, f) * p2exp ^ f * (1 - p2exp) ^ (N - f)
    log_sum += np.log(pDadj_H)

sample_bf = (np.e^log_sum_hyp1)/(np.e^log_sum_hyp2)




