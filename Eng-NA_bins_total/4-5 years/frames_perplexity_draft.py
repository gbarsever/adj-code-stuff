#!/usr/bin/python
from __future__ import division
'''
import re
import os
import itertools
from itertools import groupby
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import *
import scikits.bootstrap as bootstrap
import operator
from scipy.special import comb #comb(N,k, exact=False)
from collections import OrderedDict
'''

a_test_seq = ['a**1 b**2','g**2 b**2 h**1']
a_train_seq = ['t**1 r**2 p**1','g**2 b**2 h**1','t**1 r**2 c**1 d**3','f**2 b**1 c**1', 'k**2']

#need to toggle whether everything is .islower()


test_seq = [x.split() for x in a_test_seq]
train_seq = [x.split() for x in a_train_seq]



#should be able to take in the same data set and run the categories and frames analysis (the frames analysis just ignoring


#test_seq = ['this**Det is**Verb a**Det test**', 'i**Pro love**Verb dogs**Noun', 'tom_hiddleston**Noun needs**Verb to**Inf do**Verb less**Adj']
#train_seq = ['this**Det is**Verb a**Det test**', 'i**Pro love**Verb dogs**Noun', 'tom_hiddleston**Noun needs**Verb to**Inf do**Verb less**Adj']

#add_utt_bounds = 0
#add_utt_bounds = raw_input("include utterance boundaries? input y/n \n")
#use_1_word_utts = raw_input("include one word utterances? input y/n \n")

#for testing
add_utt_bounds = 'y'
use_1_word_utts = 'y'


#this adds in "start" and "end" to every utterance
if add_utt_bounds == 'y':
    for indx, x in enumerate(test_seq):
        test_seq[indx] = ['<s>'] + test_seq[indx] + ['</s>'] #test_seq[indx] = '<s> ' + x + ' <\s>'
    for indx, x in enumerate(train_seq):
        train_seq[indx] = ['<s>'] + train_seq[indx] + ['</s>']  #train_seq[indx] = '<s> ' + x + ' <\s>'
    if use_1_word_utts == 'y':
        utt_limit = 3
    else:
        utt_limit = 4
else:
    utt_limit = 3

#print test_seq
frames_test_seq = []
frames_train_seq = []

for utt in test_seq:
    if len(utt) >= utt_limit:
        new_frame_utt = []
        new_frame_utt.append(utt[0])
        for indy, y in enumerate(utt):
            frame_unit_1 = utt[indy].split('**')[0]  # grabs a_c out of  'a**1 b**2 c**1'
            frame_unit_2 = utt[indy + 2].split('**')[0]  # grabs a_c out of  'a**1 b**2 c**1'
            middle = utt[indy + 1].split('**')[0]
            frame = frame_unit_1 + '_' + frame_unit_2
            new_unit = middle + '**' + frame
            new_frame_utt.append(new_unit)
            #print new_unit
            if indy == len(utt)-3:
                break
        new_frame_utt.append(utt[-1])
        frames_test_seq.append(new_frame_utt)


for utt in train_seq:
    if len(utt) >= utt_limit:
        new_frame_utt = []
        new_frame_utt.append(utt[0])
        for indy, y in enumerate(utt):
            frame_unit_1 = utt[indy].split('**')[0]  # grabs a_c out of  'a**1 b**2 c**1'
            frame_unit_2 = utt[indy + 2].split('**')[0]  # grabs a_c out of  'a**1 b**2 c**1'
            middle = utt[indy + 1].split('**')[0]
            frame = frame_unit_1 + '_' + frame_unit_2
            new_unit = middle + '**' + frame
            new_frame_utt.append(new_unit)
            #print new_unit
            if indy == len(utt)-3:
                break
        new_frame_utt.append(utt[-1])
        frames_train_seq.append(new_frame_utt)

print frames_test_seq


#need to create frame dictionary from training

#emission dictionaries (with tokens)
frame_dict = {}
cat_dict = {}


for utt in train_seq:
    if len(utt) >= utt_limit:
        index = 0
        #if index+2 < len(utt): #check this!!
            #print len(utt)
        for indy,y in enumerate(utt):
            index = indy
            frame_unit_1 = utt[indy].split('**')[0] #grabs a_c out of  'a**1 b**2 c**1'
            frame_unit_2 = utt[indy+2].split('**')[0]  # grabs a_c out of  'a**1 b**2 c**1'
            middle = utt[indy+1].split('**')[0]
            frame = frame_unit_1 + '_' + frame_unit_2
            #word = utt[indy].split('**')[0] #making it middle assumes utt bounds for the cat version
            word_cat = utt[indy+1].split('**')[1]
            if frame not in frame_dict.keys():
                frame_dict[frame] = [middle]
            else:
                temp = frame_dict[frame]
                temp.append(middle)
                frame_dict[frame] = temp
            if word_cat not in cat_dict.keys():
                cat_dict[word_cat] = [middle]
            else:
                temp = cat_dict[word_cat]
                temp.append(middle)
                cat_dict[word_cat] = temp
            index = indy
            if index == len(utt)-3:
                break

#not only need frames and cats, need the counts of how many times they follow each other, etc.
list_frames = frame_dict.keys()

print frame_dict

# need to make frame dict have FREQ frames
# if word not in FF then it is assigned a snowflake category (which is just the word itself,
# i guess some snowflakes may be bigger than others?



#need to get table for transitional probs


