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
from scipy import *
import scikits.bootstrap as bootstrap
import operator
from scipy.special import comb #comb(N,k, exact=False)
from collections import OrderedDict


#CIs = bootstrap.ci(data=x,statfunction= scipy.mean) #x is the dataset (nsamples = 10,000), 95%

# want to track mean distance from noun of all adjectives
# so first make all files in to a list of lists(which will be sentences, split by whitespace)
# postition of noun-position of adj
# dictionary of adjs with values as the position
# take average


#new notes 10/18/17: preprocess so that stupid "real" is gone, check maybe for other weirdnesses.  only use intersection of adjs we have scores for
#need to check which adjs were left out, maybe run sub scores for them?
#do redupication ok and non-reduplication ok (this means in non-redup, take adjx tokens out of token counts for metric calc)



all_adjs = []


f3 = csv.reader(open('adjs_produced_copy.csv', 'rU'))
y_d3 = list(list(itertools.takewhile(lambda x: x is not None, column))
     for column in itertools.izip_longest(*f3))

new_p = []
for x in y_d3:
    new_x = []
    for word in x:
        if word == '':
            pass
        else:
            new_x.append(word.replace('?',''))
    new_p.append(new_x)

f2 = csv.reader(open('adjs_overlap_copy.csv', 'rU'))
y_d2 = list(list(itertools.takewhile(lambda x: x is not None, column))
     for column in itertools.izip_longest(*f2))

new_o = []
for x in y_d2:
    new_x = []
    for word in x:
        if word == '':
            pass
        else:
            new_x.append(word.replace('?',''))
    new_o.append(new_x)

#added 'slime'
#added 'crust'?
f = csv.reader(open('adjs_directed_copy.csv', 'rU'))
y_d = list(list(itertools.takewhile(lambda x: x is not None, column))
     for column in itertools.izip_longest(*f))

new_d = []
for x in y_d:
    new_x = []
    for word in x:
        if word == '':
            pass
        else:
            new_x.append(word.replace('?',''))
    new_d.append(new_x)

#print new_d

#all adjectives with their semantic class (and all the other ones, ah well)
for x in new_d:
    new_class = x
    for y in new_p:
        if x[0] == y[0]:
            for word in y:
                if word not in new_class:
                    new_class.append(word)
    all_adjs.append(new_class)



f = csv.reader(open('corpus_adjs.csv', 'rU'))
y_d = list(list(itertools.takewhile(lambda x: x is not None, column))
     for column in itertools.izip_longest(*f))

new_all = []
for x in y_d:
    new_x = []
    for word in x:
        if word == '':
            pass
        else:
            new_x.append(word.replace('?','').lower())
    new_all.append(new_x)



all_da_utts = []
c_directed = []
c_produced = []
#dict = {'cats':['tiger','leopards','jaguars'], 'dogs': [...]}

d_all_rough = []
p_all_rough = []
dup_or_not = raw_input("include duplicate adjs? (e.g. \'wee wee wee kitty\'. enter y for yes or n for no\n")
binned_or_not = raw_input("use binned classes?\n")
other_or_not = raw_input("use class \'other\'?")
#folder = raw_input("pick a folder: Eng-NA or Eng-UK")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f[0] == '+':
        infile = open(f, 'r')
        reading = infile.read()
        p_all_rough.append(reading.replace('\n', '').split("----------------------------------------"))
        #rough = re.findall(r'%mor:.+\.',reading,re.MULTILINE)
        #rough2 = re.findall(r'%mor:.+\?',reading,re.MULTILINE)
        #rough3 = re.findall(r'%mor:.+!',reading,re.MULTILINE)
        #if rough != []:
            #p_all_rough.append(rough) #changed from append
        #if rough2 != []:
            #p_all_rough.append(rough2)
        #if rough3 != []:
            #p_all_rough.append(rough3)
        ##rough = re.findall(r'%mor:.+\.|\?|!', reading, re.MULTILINE)
        ##p_all_rough.extend(rough) #changed from append

    elif f[0] == '-':
        infile = open(f, 'r')
        reading = infile.read()
        d_all_rough.append(reading.replace('\n', '').split("----------------------------------------"))
        #rough = re.findall(r'%mor:.+\.',reading,re.MULTILINE)
        #rough2 = re.findall(r'%mor:.+\?',reading,re.MULTILINE)
        #rough3 = re.findall(r'%mor:.+!',reading,re.MULTILINE)
        #if rough != []:
            #d_all_rough.append(rough) #changed from append
       # if rough2 != []:
            #d_all_rough.append(rough2)
        #if rough3 != []:
            #d_all_rough.append(rough3)
#print d_all_rough[0:20]

                #split_thing = thing.split()
                #c_directed.append(split_thing)
                #all_da_utts.append(split_thing)
        #all_mor = re.findall(r'mor:.+\.|\?|\!?', readinfile)


    # deal with '~', '&', '-', CAPS character (other weirdos)

for sentence in p_all_rough:
    # deal with '~', '&', '-', CAPS character (other weirdos)
    temp = []
    for word1 in sentence:
        y = re.findall(r'[a-z]+:*[a-z]*\|[a-z]+', word1, re.MULTILINE)
        if not y:
            pass
        else:
            temp.extend(y)
    if not temp:
        continue
    else:
        c_produced.append(temp)
for sentence in d_all_rough:
    temp = []
    #print sentence
    for word2 in sentence:
        #print word2
        y = re.findall(r'[a-z]+:*[a-z]*\|[a-z]+', word2, re.MULTILINE)
        if not y:
            pass
        else:
            temp.extend(y)
            #print temp
    if not temp:
        continue
    else:
        c_directed.append(temp)
'''
for word1 in p_all_rough:
    temp = []
    y = re.findall(r'[a-z]+:*[a-z]*\|[a-z]+', word1, re.MULTILINE)
    if not y:
        pass
    else:
        temp.extend(y)
    if not temp:
        continue
    else:
        c_produced.append(temp)
for sentence in d_all_rough:
    temp = []
    y = re.findall(r'[a-z]+:*[a-z]*\|[a-z]+', sentence, re.MULTILINE)
    if not y:
        pass
    else:
        temp.extend(y)
            #print temp
    if not temp:
        continue
    else:
        c_directed.append(temp)
        '''
#print c_directed[0:5]

#print "# pro utts: ", len(c_produced)
#print "# dir utts: ", len(c_directed)
def remove_adjacent(seq): # works on any sequence, not just on numbers
  i = 1
  n = len(seq)
  while i < n: # avoid calling len(seq) each time around
    if seq[i] == seq[i-1]:
      del seq[i]
      # value returned by seq.pop(i) is ignored; slower than del seq[i]
      n -= 1
    else:
      i += 1
  #### return seq #### don't do this
  # function acts in situ; should follow convention and return None

test_seq = [['v|sing','adj|one','adj|little','adj|little','adj|baby','adj|blue','n|bird',
             'v|blah','n|ball'],['adj|one','adj|one','adj|green','n|two','adj|opaline','adj|gemlike','n|jewels']]

#for x in test_seq:
#    remove_adjacent(x)
# print test_seq

#deal with duplicate flag here: compress adjs that are duplicated before even calculate them
if dup_or_not == 'n':
    #new_c_directed = []
    for utt in c_directed:
        remove_adjacent(utt)
        #new_c_directed.append([k for k, g in itertools.groupby(utt)])
    #c_directed = new_c_directed
    #new_c_produced = []
    for utt in c_produced:
        remove_adjacent(utt)
        #new_c_produced.append([k for k, g in itertools.groupby(utt)])
        #print "new produced", new_c_produced[0]
    #c_produced = new_c_produced


#print test_seq

#print ("DIS!",len(d_all_rough))
c_d_dict = dict()
c_p_dict = dict()
count_d = 0
count_p = 0
adj_seq_list_d = []
adj_seq_list_p = []
for utt in c_directed: #c_directed
    for word in utt:
        #print word
        word_split = word.split('|')
        if word_split[0] == 'n':
            temp_list = []
            n_pos = utt.index(word)
            previous_word = utt[n_pos-1]
            previous_split = previous_word.split('|')
            while utt[n_pos-1].split('|')[0] == 'adj' and n_pos-1 != -1:
                prev_split = previous_word.split('|')
                temp_list.append(prev_split[1])
                n_pos-=1
                previous_word = utt[n_pos - 1]
                #print n_pos
            if len(temp_list) > 1:
                adj_seq_list_d.append(temp_list)

new_adj_seq_list_d = [] #should be 1away[0] and 2away[1]
for strang in adj_seq_list_d: #this is making sure only 2 adj-strings
    if len(strang) == 2:
        new_adj_seq_list_d.append(strang)
    else:
        new_adj_seq_list_d.append([strang[0],strang[1]])

#put here a way to compare how many adj strings there were originally and how many we are using

adj_seq_list_d = new_adj_seq_list_d


for utt in c_produced:
    for word in utt:
        #print word
        word_split = word.split('|')
        if word_split[0] == 'n':
            temp_list = []
            n_pos = utt.index(word)
            previous_word = utt[n_pos-1]
            previous_split = previous_word.split('|')
            while utt[n_pos-1].split('|')[0] == 'adj' and n_pos-1 != -1:
                prev_split = previous_word.split('|')
                temp_list.append(prev_split[1])
                n_pos-=1
                previous_word = utt[n_pos - 1]
                #print n_pos
            if len(temp_list) > 1:
                adj_seq_list_p.append(temp_list)

#print adj_seq_list_p

#print p_all_rough
new_adj_seq_list_p = []
for strang in adj_seq_list_p:
    if len(strang) == 2:
        new_adj_seq_list_p.append(strang)
    else:
        new_adj_seq_list_p.append([strang[0],strang[1]])

adj_seq_list_p = new_adj_seq_list_p

new_container = []
for x in adj_seq_list_p:
    new_container.append(x[0])
    new_container.append(x[1])
for y in adj_seq_list_d:
    new_container.append(y[0])
    new_container.append(y[1])

new_container_set = set(new_container)

print len(new_container_set), "ALL ADJ TYPES"


#this will just get the set of all the adj types

#adjust seq lists and c dicts up here
#need to preprocess the multi-adj strings before they get to calculation time.
#both adjs in str must have class and subjectivity scores
#get rid of "real good"
#~~~~~~~~~~~~~~~~~

subjectivity_dict = {}
subjectivity_dict_av = {}
with open('adjective-subjectivity.csv', 'rU') as csvfile: #2nd column adj, 4th column response (dont need to be averaged)
    reader = csv.DictReader(csvfile)
    for element in reader:
        adj = element['predicate'].lower()
        if adj not in subjectivity_dict.keys():
            subjectivity_dict[adj] = float(element['response'])

prep_adj_seq_list_d = []
prep_adj_seq_list_p = []
old_adj_list_d = adj_seq_list_d #flat_list = [item for sublist in l for item in sublist]
old_adj_list_p = adj_seq_list_p

old_c_d_dict = {}
old_c_p_dict = {}

for adj_seq in old_adj_list_d:
    for word in set(adj_seq):
        if word in old_c_d_dict:
            temp = old_c_d_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            old_c_d_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]


for adj_seq in old_adj_list_p:
    for word in set(adj_seq):
        if word in old_c_p_dict:
            temp = old_c_p_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            old_c_p_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]




for couple in adj_seq_list_d:
    if couple[1] == 'brand' or couple[1] == 'real':
        pass
    elif couple == ['cross', 'hot']:
        pass
    else:
        prep_adj_seq_list_d.append(couple)

for couple in adj_seq_list_p:
    if couple[1] == 'brand' or couple[1] == 'real':
        pass
    elif couple == ['cross', 'hot']:
        pass
    else:
        prep_adj_seq_list_p.append(couple)


#a=[1,2,3,1,3,2,1,1]
#[4 if x==1 else x for x in a]
interim_d = []
for adj_string in prep_adj_seq_list_d:
    new_word = ['lovely' if x == 'love' else x for x in adj_string]
    new_word1 = ['scary' if x == 'scare' else x for x in new_word]
    new_word2 = ['dirty' if x == 'dirt' else x for x in new_word1]
    new_word3 = ['cozy' if x == 'cosy' else x for x in new_word2]
    new_word4 = ['curly' if x == 'curl' else x for x in new_word3]
    new_word5 = ['grey' if x == 'gray' else x for x in new_word4]
    new_word6 = ['yucky' if x == 'yuck' else x for x in new_word5]
    new_word7 = ['fluffy' if x == 'fluff' else x for x in new_word6]
    new_word8 = ['teeny' if x == 'teenie' else x for x in new_word7]
    new_word9 = ['weeny' if x == 'weenie' else x for x in new_word8]
    interim_d.append(new_word9)
    #print new_word7


interim_p = []
for adj_string in prep_adj_seq_list_p:
    new_word = ['lovely' if x == 'love' else x for x in adj_string]
    new_word1 = ['scary' if x == 'scare' else x for x in new_word]
    new_word2 = ['dirty' if x == 'dirt' else x for x in new_word1]
    new_word3 = ['cozy' if x == 'cosy' else x for x in new_word2]
    new_word4 = ['curly' if x == 'curl' else x for x in new_word3]
    new_word5 = ['grey' if x == 'gray' else x for x in new_word4]
    new_word6 = ['yucky' if x == 'yuck' else x for x in new_word5]
    new_word7 = ['fluffy' if x == 'fluff' else x for x in new_word6]
    new_word8 = ['teeny' if x == 'teenie' else x for x in new_word7]
    new_word9 = ['weeny' if x == 'weenie' else x for x in new_word8]
    interim_p.append(new_word9)

#adj_seq_list_p = prep_adj_seq_list_p
#adj_seq_list_d = prep_adj_seq_list_d
#new_all has lexical class info

final_adj_list_p = []
final_adj_list_d = []
other = []
for thing in new_all:
    if thing[0] == 'other':
        other = thing[1:]

#adjust this to get subjectivity vs baseline, just need to get counts for subjecitvity but dont have to be paired with something that has a subjectivity score
for couple in interim_d:
    if other_or_not == 'y':
        if couple[0] in subjectivity_dict.keys() and couple[1] in subjectivity_dict.keys():
            final_adj_list_d.append(couple)
    else:
        if couple[0] in subjectivity_dict.keys() and couple[1] in subjectivity_dict.keys():
            if couple[0] not in other and couple[1] not in other:
                final_adj_list_d.append(couple)

for couple in interim_p:
    if other_or_not == 'y':
        if couple[0] in subjectivity_dict.keys() and couple[1] in subjectivity_dict.keys():
            final_adj_list_p.append(couple)

    else:
        if couple[0] in subjectivity_dict.keys() and couple[1] in subjectivity_dict.keys():
            if couple[0] not in other and couple[1] not in other:
                final_adj_list_p.append(couple)


adj_seq_list_d = final_adj_list_d
adj_seq_list_p = final_adj_list_p

print "age 2, this how many total adj strings directed", len(interim_d)
print "how many produced", len(interim_p)
print "how many used for hypothesis testing directed", len(final_adj_list_d)
print "how many used for hypothesis testing produced", len(final_adj_list_p)

#print adj_seq_list_d[0:4]
#scare->scary, dirt->dirty , cosy-> cozy, yuck->yucky, curl -> curly, gray -> grey(brand, real)
#cross is in "hot cross buns",
#love-> lovely,  fluff->fluffy
#print subjectivity_dict['lovely'] #dont have a score for lovely

#~~~~~~~~~~~~~~~~~


for adj_seq in adj_seq_list_d:
    for word in set(adj_seq):
        if word in c_d_dict:
            temp = c_d_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            c_d_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]


for adj_seq in adj_seq_list_p:
    for word in set(adj_seq):
        if word in c_p_dict:
            temp = c_p_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            c_p_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]


#outfile_include_sets = open('adj-seq-difference.txt')
############
interim_c_d_dict = {}
interim_c_p_dict = {}

for adj_seq in final_adj_list_d:
    for word in set(adj_seq):
        if word in interim_c_d_dict:
            temp = interim_c_d_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            interim_c_d_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]


for adj_seq in final_adj_list_p:
    for word in set(adj_seq):
        if word in interim_c_p_dict:
            temp = interim_c_p_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            interim_c_p_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]

print 'directed adj seqs both have subjectivity', len(adj_seq_list_d)
print 'directed adj seqs both have subjectivity', len(adj_seq_list_d)
############
#need actual size of corpus used
#flag for include reduplication, not include....


list_adjs_paper = [['old','new','rotten','fresh'],['red','yellow','green',
                   'blue','purple','brown'],['wooden','plastic','metal'],['good',
                   'bad'],['round','square'],['big','small','huge','tiny','short',
                   'long'],['smooth','hard','soft']]

print "# adjs types in produced: ", len(interim_c_p_dict)
print "# adjs types in directed: ", len(interim_c_d_dict)

flat_cp = [item for sublist in interim_c_p_dict.values() for item in sublist]
flat_cd = [item for sublist in interim_c_d_dict.values() for item in sublist]
print "# adj tokens in produced: ", len(flat_cp)
print "# adj tokens in directed: ", len(flat_cd)


#~~~~~~~~~~~~~~~~~
list_adjs_p = sorted(c_p_dict, key=lambda k: len(c_p_dict[k]), reverse=True)
list_adjs_d = sorted(c_d_dict, key=lambda k: len(c_d_dict[k]), reverse=True)

interim_list_adjs_p = sorted(interim_c_p_dict, key=lambda k: len(interim_c_p_dict[k]), reverse=True)
interim_list_adjs_d = sorted(interim_c_d_dict, key=lambda k: len(interim_c_d_dict[k]), reverse=True)
'''
if other_or_not == 'n':
    new_interim_list_all_adjs_p = []
    for x in interim_list_adjs_p:
        if x in other:
            pass
        else:
            new_interim_list_all_adjs_p.append(x)
    new_interim_list_all_adjs_d = []

    for x in interim_list_adjs_d:
        if x in other:
            pass
        else:
            new_interim_list_all_adjs_d.append(x)
    interim_list_adjs_p = new_interim_list_all_adjs_p
    interim_list_adjs_d = new_interim_list_all_adjs_d
'''
print "age 2-4 adj-seq directed", len(adj_seq_list_d)
print "age 2-4 adj-seq produced", len(adj_seq_list_p)
print "age 2-4 # adj types directed", len(list_adjs_d)
print "age 2-4 # adj types produced", len(list_adjs_p)


outfile_adjs = open('2adjs_exp.txt', 'w')
outfile_adjs.write("Adjectives in child directed and child produced English from 2-4 with frequencies:\n")
outfile_adjs.write("Directed:\n~~~~~~~~~~~~~~\n")
for x in list_adjs_d:
    outfile_adjs.write("("+str(len(c_d_dict[x]))+") ")
    outfile_adjs.write(x)
    outfile_adjs.write("\n")
outfile_adjs.write("\nProduced:\n~~~~~~~~~~~~~~\n")

for x in list_adjs_p:
    outfile_adjs.write("(" + str(len(c_p_dict[x])) + ") ")
    outfile_adjs.write(x)
    outfile_adjs.write("\n")
outfile_adjs.close()

new_dict_all_adjs_d = dict()
new_dict_all_adjs_p = dict()

mean_cd = dict()
mean_cp = dict()
for adj in c_d_dict:
    mean_cd[adj] = sum(c_d_dict[adj]) / float(len(c_d_dict[adj]))
for adj in c_p_dict.keys():
    mean_cp[adj] = sum(c_p_dict[adj]) / float(len(c_p_dict[adj]))

for x in list_adjs_d:
    for y in new_all:
        if x in y:
            sem_label = y[0]
    new_dict_all_adjs_d[x] = [len(c_d_dict[x]), sem_label]

for x in list_adjs_p:
    for y in new_all:
        if x in y:
            sem_label = y[0]
    new_dict_all_adjs_p[x] = [len(c_p_dict[x]), sem_label]
#print new_dict_all_adjs_p

###############

interim_mean_cd = dict()
interim_mean_cp = dict()
interim_new_dict_all_adjs_d = {}
interim_new_dict_all_adjs_p = {}
for adj in interim_c_d_dict:
    interim_mean_cd[adj] = sum(interim_c_d_dict[adj]) / float(len(interim_c_d_dict[adj]))
for adj in interim_c_p_dict.keys():
    interim_mean_cp[adj] = sum(interim_c_p_dict[adj]) / float(len(interim_c_p_dict[adj]))

for x in interim_list_adjs_d:
    for y in new_all:
        if x in y:
            sem_label = y[0]
    interim_new_dict_all_adjs_d[x] = [len(interim_c_d_dict[x]), sem_label]

for x in interim_list_adjs_p:
    for y in new_all:
        if x in y:
            sem_label = y[0]
    interim_new_dict_all_adjs_p[x] = [len(interim_c_p_dict[x]), sem_label]

###############

c3 = [val for val in c_p_dict.keys() if val in c_d_dict.keys()]
#print(c3)
#print(len(c3)) #this is length of the overlap

binned_classes = [['value'],['dimension', 'age', 'physical'],['shape', 'color', 'material']] #value, dimension age physical, shape color material (with other plot for color maybe)
#print all_adjs
semanticClassDict_p = dict()  # key is class (which is the first element of list, value is average and CIs
for semanticclass in new_all:
    #print semanticclass
    semanticclasslist_p = []
    #if semanticclass[0] != 'other':  #get rid of other category
    for word in semanticclass[1:]:
        if word in interim_c_p_dict:
            semanticclasslist_p.extend(interim_c_p_dict[word])
    if semanticclasslist_p != []:
        #print semanticclass[0], semanticclasslist_p
        if len(set(semanticclasslist_p)) != 1:
            CIs = bootstrap.ci(data=semanticclasslist_p, statfunction=scipy.mean)
            mean_class_p = scipy.mean(semanticclasslist_p)
            #print mean_class_p
            semanticClassDict_p[semanticclass[0]] = [mean_class_p, CIs[0], CIs[1], len(semanticclasslist_p)]
        else:
            mean_class_p = scipy.mean(semanticclasslist_p)
            semanticClassDict_p[semanticclass[0]] = [mean_class_p, mean_class_p, mean_class_p, len(semanticclasslist_p)]

#for x in semanticClassDict_p:
    #print x,  ',',semanticClassDict_p[x][0]

semanticClassDict_d = dict() #key is class (which is the first element of list, value is average
for semanticclass in new_all:
    semanticclasslist = []
    #if semanticclass[0] != 'other':  #get rid of other category
    for word in semanticclass[1:]:
        if word in interim_c_d_dict:
            semanticclasslist.extend(interim_c_d_dict[word])
    if semanticclasslist != []:
        #print semanticclasslist
        if len(set(semanticclasslist)) != 1:
            #bootstrap.ci doesnt like it when there is only 1 unique element in dataset
            CIs = bootstrap.ci(data=semanticclasslist, statfunction=scipy.mean)
            mean_class = scipy.mean(semanticclasslist)
            semanticClassDict_d[semanticclass[0]] = [mean_class, CIs[0], CIs[1], len(semanticclasslist)]
        else:
            #print semanticclasslist
            mean_class = scipy.mean(semanticclasslist)
            semanticClassDict_d[semanticclass[0]] = [mean_class, mean_class, mean_class, len(semanticclasslist)]

#for x in semanticClassDict_d:
    #print x, ',', semanticClassDict_d[x][0]

'''
semanticClassDict_d_binned = dict()
semanticClassDict_p_binned = dict()
for bin in binned_classes:
    binned_list_d = []
    binned_list_p = []
    key = "-".join(bin)
    for thing in bin:
        for semanticclass in new_all:
            if thing == semanticclass[0]:
                for word in semanticclass[1:]:
                    if word in c_d_dict:
                        binned_list_d.extend(c_d_dict[word])
                    if word in c_p_dict:
                        binned_list_p.extend(c_p_dict[word])
    if binned_list_d != []:
        if len(set(binned_list_d)) != 1:
            CIs = bootstrap.ci(data=binned_list_d, statfunction=scipy.mean)
            mean_class = scipy.mean(binned_list_d)
            semanticClassDict_d_binned[key] = [mean_class, CIs[0], CIs[1], len(binned_list_d)]
        else:
            mean_class = scipy.mean(binned_list_d)
            semanticClassDict_d_binned[key] = [mean_class, mean_class, mean_class, len(binned_list_d)]
    if binned_list_p != []:
        if len(set(binned_list_p)) != 1:
            CIs = bootstrap.ci(data=binned_list_p, statfunction=scipy.mean)
            mean_class = scipy.mean(binned_list_p)
            semanticClassDict_p_binned[key] = [mean_class, CIs[0], CIs[1], len(binned_list_p)]
        else:
            mean_class = scipy.mean(binned_list_p)
            semanticClassDict_p_binned[key] = [mean_class, mean_class, mean_class, len(binned_list_p)]
'''

#print "NOW BINNED\n"
#print semanticClassDict_d_binned

#print semanticClassDict_d_binned
print '~~~~~~~~~'
#print semanticClassDict_p_binned

#print semanticClassDict_d #do the others

#~~~~~big list for greg~~~~~~

#need to do csv writer: need
#word
#average distance, need mean_cd or mean_cp
#overlap with greg's big list (0 no, 1 yes)
#age, just put in each folder
#produced or directed

#need to get semantic class of adj, create seperate dictionary, then put in file:
#print all_adjs, "wheeeeeeee"
adj_class_dict_d = dict()
adj_class_dict_p = dict()

#this is the wrong dict i think
for adj in c_d_dict.keys():
    for sem_class in new_all:
        if adj in sem_class[1:]:
            adj_class_dict_d[adj] = sem_class[0]

for adj in c_p_dict.keys():
    for sem_class in new_all:
        if adj in sem_class[1:]:
            adj_class_dict_p[adj] = sem_class[0]



flat_ex1 = [item for sublist in list_adjs_paper for item in sublist]

flat_list = [item for sublist in new_all for item in sublist]
'''
for x in mean_cp.keys():
    if x not in flat_list:
        print x
print "^^^"
for x in mean_cd.keys():
    if x not in flat_list:
        print x
print "^^^"

'''
#print adj_class_dict_d
#print adj_class_dict_p

#need list of lists with BIG_LIST = [[w1,w2,w3,w4],[w5,w5,w6]...]  or
#actually just need B_L = [4,6,9, etc]
#  where the bins are in order.  tokens less that are BIG_LIST[:pos] and equal to are BIG_LIST[pos]
#c_d_dict and c_p_dict have the token information implicitly ({adj: [1,1,1,0]})
#binned_classes = [['value'],['dimension', 'age', 'physical'],['shape', 'color', 'material']]
#adj_class_dict_d has word/class info
# new_dict_all_adjs_d has adj(key), freq, sem class

#need to adjust classes with new classifications
#class orders will differ depending on corpus!




#classes = ['value','human','dimension', 'physical','speed', 'age', 'temporal', 'location', 'color','shape', 'material']#['value','dimension', 'age', 'physical','shape', 'color', 'material'] NEED TO FLIP THESE!! *CLOSER* SEMANTIC CLASS!!!
#class_pos = {'value':0,'dimension':1, 'age':2, 'physical':3,'shape':4, 'color':5, 'material':6, 'other':100}
#binned_class_pos = {'value':0,'dimension':1, 'age':1, 'physical':1,'shape':2, 'color':2, 'material':2, 'other':100}

#read in subjectivity results (also make everything lowercase)

        #else:
            #temp = subjectivity_dict[adj]
            #temp = temp.append(float(element['response']))
            #subjectivity_dict[adj] = temp
old_grey = subjectivity_dict['grey']
subjectivity_dict['grey'] = (old_grey + subjectivity_dict['gray'])/2



sub_dict_p = {} #score: in sub tokens, less sub tokens tokens
sub_dict_d = {}
for adj in subjectivity_dict.keys():
    score = subjectivity_dict[adj]
    if adj in new_dict_all_adjs_d.keys():
        adj_tokens = new_dict_all_adjs_d[adj][0]
        #print adj, adj_tokens
        if score not in sub_dict_d.keys():
            sub_dict_d[score] = [adj_tokens, 0]
            #print sub_dict_d[score]
        else:
            in_tokens = sub_dict_d[score][0]
            sub_dict_d[score] = [(in_tokens + new_dict_all_adjs_d[adj][0]), 0]
            #print sub_dict_d[score]
        #print score
#print sub_dict_d
#print sub_dict_d[0.935714285714]
#sys.exit()
for adj in subjectivity_dict.keys():
    score = subjectivity_dict[adj]
    if adj in new_dict_all_adjs_p.keys():
        adj_tokens = new_dict_all_adjs_p[adj][0]
        if score not in sub_dict_p.keys():
            sub_dict_p[score] = [adj_tokens, 0]
        else:
            in_tokens = sub_dict_p[score][0]
            sub_dict_p[score] = [(in_tokens + adj_tokens), 0]

for score1 in sub_dict_d.keys():
    in_tokens = sub_dict_d[score1][0]
    for score2 in sub_dict_d.keys():
        score2_tokens = sub_dict_d[score2][0]
        less_score = sub_dict_d[score1][1]
        if score2 < score1:
            less_score += score2_tokens
            sub_dict_d[score1] = [in_tokens, less_score]

for score1 in sub_dict_p.keys():
    in_tokens = sub_dict_p[score1][0]
    for score2 in sub_dict_p.keys():
        score2_tokens = sub_dict_p[score2][0]
        less_score = sub_dict_p[score1][1]
        if score2 < score1:
            less_score += score2_tokens
            sub_dict_p[score1] = [in_tokens, less_score]

#print sub_dict_p
#sorted_sub_p = OrderedDict(sorted(sub_dict_p.items()))
#print sorted_sub_p
######################

interim_sub_dict_p = {} #score: in sub tokens, less sub tokens tokens
interim_sub_dict_d = {}
for adj in subjectivity_dict.keys():
    score = subjectivity_dict[adj]
    if adj in interim_new_dict_all_adjs_d.keys():
        adj_tokens = interim_new_dict_all_adjs_d[adj][0]
        #print adj, adj_tokens
        if score not in interim_sub_dict_d.keys():
            interim_sub_dict_d[score] = [adj_tokens, 0]
            #print sub_dict_d[score]
        else:
            in_tokens = interim_sub_dict_d[score][0]
            interim_sub_dict_d[score] = [(in_tokens + interim_new_dict_all_adjs_d[adj][0]), 0]
            #print sub_dict_d[score]
        #print score
#print sub_dict_d
#print sub_dict_d[0.935714285714]
#sys.exit()
for adj in subjectivity_dict.keys():
    score = subjectivity_dict[adj]
    if adj in interim_new_dict_all_adjs_p.keys():
        adj_tokens = interim_new_dict_all_adjs_p[adj][0]
        if score not in interim_sub_dict_p.keys():
            interim_sub_dict_p[score] = [adj_tokens, 0]
        else:
            in_tokens = interim_sub_dict_p[score][0]
            interim_sub_dict_p[score] = [(in_tokens + adj_tokens), 0]

for score1 in interim_sub_dict_d.keys():
    in_tokens = interim_sub_dict_d[score1][0]
    for score2 in interim_sub_dict_d.keys():
        score2_tokens = interim_sub_dict_d[score2][0]
        less_score = interim_sub_dict_d[score1][1]
        if score2 < score1:
            less_score += score2_tokens
            interim_sub_dict_d[score1] = [in_tokens, less_score]

for score1 in interim_sub_dict_p.keys():
    in_tokens = interim_sub_dict_p[score1][0]
    for score2 in interim_sub_dict_p.keys():
        score2_tokens = interim_sub_dict_p[score2][0]
        less_score = interim_sub_dict_p[score1][1]
        if score2 < score1:
            less_score += score2_tokens
            interim_sub_dict_p[score1] = [in_tokens, less_score]

#sorted_sub_p = OrderedDict(sorted(interim_sub_dict_p.items()))
#sorted_sub_d = OrderedDict(sorted(interim_sub_dict_d.items()))

sorted_sub_d = sorted(interim_sub_dict_d)#, key=interim_sub_dict_d.get)


#print sorted_sub_d

#range7 = range(0,8)

#new_range7 = [x*((max(sorted_sub_d)-min(sorted_sub_d))/7) for x in range7]
#final_range7 = [x+min(sorted_sub_d) for x in new_range7]

#print final_range7
#split_bin = np.array_split(range(min(sorted_sub_d),max(sorted_sub_d)), 8) #this needs to be a range from 0-1, 7 bins, so range(1,8)/7
#split_bin14 = np.array_split(range(min(sorted_sub_d),max(sorted_sub_d)), 13) #this is for representation analysis
#sub_bins = []

#for thing in split_bin:
#    sub_bins.append(float(thing/7))

inv_map = {}# make so everything a list#{v: k for k, v in subjectivity_dict.iteritems()} #gets dictionary with {score: adj}
for adj in subjectivity_dict.keys():
    score = subjectivity_dict[adj]
    if score not in inv_map.keys():
        inv_map[score] = [adj]
    else:
        old = inv_map[score]
        old.append(adj)
        inv_map[score] = old

scores = inv_map.keys()
arrayify = np.array(scores)

sub_bins7 = linspace(min(inv_map.keys()),max(inv_map.keys()), 7) #needs to be over entire subjectivity scores, not just d or p
sub_bins12 = linspace(min(inv_map.keys()),max(inv_map.keys()), 12)
binned_sub_7 = np.digitize(scores, sub_bins7)
binned_sub_12 = np.digitize(scores, sub_bins12)

binned_sub_d_7_dict = {}
adj_sub_bin_d_dict = {}

#sub_bins7_p = linspace(min(sorted_sub_p),max(sorted_sub_p), 7)
#sub_bins12_p = linspace(min(sorted_sub_p),max(sorted_sub_p), 12)
#binned_sub_p_7 = np.digitize(sorted_sub_p, sub_bins7_p)
#binned_sub_p_12 = np.digitize(sorted_sub_p, sub_bins12_p)

binned_sub_p_7_dict = {}
adj_sub_bin_p_dict = {}

binned_sub_d7 = {}
binned_sub_p7 = {}
binned_sub_d12 = {}
binned_sub_p12 = {}


binned_sub_d_12_dict = {}
binned_sub_p_12_dict = {}


#adj_sub_bin_d7 = {}
#adj_sub_bin_p7 = {}
#print sub_bins


#>>> np.where(binplace == 1)
#(array([ 0,  6, 15]),)
#>>> np.where(binplace == 2)
#(array([ 2, 10, 16]),)

#>>> avgs[np.where(binplace == 1)]
#array([ 11.02,  11.3 ,  11.01])

#dont need adj dict for 7, only for 12
for pos in set(binned_sub_7):
    list_subs = arrayify[np.where(binned_sub_7 == pos)]
    count_sub = 0
    adj_sub_list = []
    for x in list_subs:
        if x in interim_sub_dict_d:
            count_sub += interim_sub_dict_d[x][0]
            for adj in inv_map[x]:
                if adj in interim_c_d_dict.keys():
                    #adj_sub_bin_d_dict[adj] = pos
                    adj_sub_list.extend(interim_c_d_dict[adj])
    binned_sub_d_7_dict[pos] = count_sub
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d7[pos] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d7[pos] = [mean_class, mean_class, mean_class, len(adj_sub_list)]

for pos in set(binned_sub_7):
    list_subs = arrayify[np.where(binned_sub_7 == pos)]
    count_sub = 0
    adj_sub_list = []
    for x in list_subs:
        if x in interim_sub_dict_p:
            count_sub += interim_sub_dict_p[x][0]
            for adj in inv_map[x]:
                if adj in interim_c_p_dict.keys():
                    #adj_sub_bin_p_dict[adj] = pos
                    adj_sub_list.extend(interim_c_p_dict[adj])
    binned_sub_p_7_dict[pos] = count_sub
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p7[pos] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p7[pos] = [mean_class, mean_class, mean_class, len(adj_sub_list)]

#print binned_sub_d_7_dict #{1: 48, 2: 264, 3: 442, 4: 227, 5: 620, 6: 137, 7: 38}
#print adj_sub_bin_d_dict #{'cute': 5, 'chinese': 1,



####for new sub bins:  Nitty-gritty, so when calculating how many tokens are less subjective,
# it will be all adjectives that are less subjective than (adj_x's subjectivity-.1).
# And the number of adjectives within the same subjectivity score is the number of adjs
# which subjectivity score falls in (adj_x's subjectivity-.1 to adj_x's subjectivity+.1 )?

point1sub_p = dict()
point1sub_d = dict()

for adj in subjectivity_dict.keys():
    sub_score = subjectivity_dict[adj]
    bottom_score = sub_score - .1
    top_score = sub_score + .1
    count_less_p = 0
    count_same_p = 0
    count_less_d = 0
    count_same_d = 0
    for x in interim_sub_dict_d.keys():
        if x <= bottom_score:
            count_less_d += interim_sub_dict_d[x][0]
            #count_less_p += interim_sub_dict_p[x][0]
        elif x > bottom_score and x <= top_score:
            count_same_d += interim_sub_dict_d[x][0]
            #count_same_p += interim_sub_dict_p[x][0]
        else:
            pass
    for x in interim_sub_dict_p.keys():
        if x <= bottom_score:
            #count_less_d += interim_sub_dict_d[x][0]
            count_less_p += interim_sub_dict_p[x][0]
        elif x > bottom_score and x <= top_score:
            #count_same_d += interim_sub_dict_d[x][0]
            count_same_p += interim_sub_dict_p[x][0]
        else:
            pass
    point1sub_d[adj] = [count_less_d, count_same_d]
    point1sub_p[adj] = [count_less_p, count_same_p]



with open('2_sub_bin_stats_w_other.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['class', 'mean', 'CI1', 'CI2', 'N', 'age', 'p/d'])
    for key, value in binned_sub_d7.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '2', 'child-directed'])
    for key, value in binned_sub_p7.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '2', 'child-produced'])



for pos in set(binned_sub_12):
    list_subs = arrayify[np.where(binned_sub_12 == pos)]
    count_sub = 0
    adj_sub_list = []
    for x in list_subs:
        if x in interim_sub_dict_d:
            count_sub += interim_sub_dict_d[x][0]
            for adj in inv_map[x]:
                if adj in interim_c_d_dict.keys():
                    adj_sub_bin_d_dict[adj] = pos
                    adj_sub_list.extend(interim_c_d_dict[adj])
    binned_sub_d_12_dict[pos] = count_sub
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d12[pos] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d12[pos] = [mean_class, mean_class, mean_class, len(adj_sub_list)]

for pos in set(binned_sub_12):
    list_subs = arrayify[np.where(binned_sub_12 == pos)]
    count_sub = 0
    adj_sub_list = []
    for x in list_subs:
        if x in interim_sub_dict_p:
            count_sub += interim_sub_dict_p[x][0]
            for adj in inv_map[x]:
                if adj in interim_c_p_dict.keys():
                    adj_sub_bin_p_dict[adj] = pos
                    adj_sub_list.extend(interim_c_p_dict[adj])
    binned_sub_p_7_dict[pos] = count_sub
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p12[pos] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p12[pos] = [mean_class, mean_class, mean_class, len(adj_sub_list)]
print binned_sub_d12

with open('2_sub_bin_stats_exp_freeorder_wother.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['class', 'mean', 'CI1', 'CI2', 'N', 'age', 'p/d'])
    for key, value in binned_sub_d12.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '2', 'child-directed'])
    for key, value in binned_sub_p12.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '2', 'child-produced'])

#print interim_c_p_dict['beautiful']

'''
#print inv_map
#sub_bins = final_range7[1:]
checked_bins_d = min(final_range7)
for bin in sub_bins:
    adj_sub_list = []
    #temp = 0
    for x in inv_map.keys():
        #print x
        #break
        if x < bin and x >= checked_bins_d:
            #temp += interim_sub_dict_d[x][0]
            adj = inv_map[x]
            #print adj
            if adj in interim_new_dict_all_adjs_d.keys(): #interim_new_dict_all_adjs_d
                adj_sub_list.extend(interim_c_d_dict[adj])
                #print bin
                adj_sub_bin_d[adj] = bin
    #print bin
    checked_bins_d = bin
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d[bin] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_d[bin] = [mean_class, mean_class, mean_class, len(adj_sub_list)]
#print len(adj_sub_bin_d), len(interim_new_dict_all_adjs_d)
#print interim_new_dict_all_adjs_d['next']
#print subjectivity_dict['busy']
#adj_sub_bin_d['busy'] = 0.8571428571428571
checked_bins_p = 0
for bin in sub_bins:
    adj_sub_list = []
    # temp = 0
    for x in interim_sub_dict_p.keys():
        if x <= bin and x > checked_bins_p:
        # temp += interim_sub_dict_d[x][0]
            adj = inv_map[x]
            if adj in interim_new_dict_all_adjs_p.keys():
                adj_sub_list.extend(interim_c_p_dict[adj])
    checked_bins_p = bin
    if adj_sub_list != []:
        if len(set(adj_sub_list)) != 1:
            CIs = bootstrap.ci(data=adj_sub_list, statfunction=scipy.mean)
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p[bin] = [mean_class, CIs[0], CIs[1], len(adj_sub_list)]
        else:
            # print semanticclasslist
            mean_class = scipy.mean(adj_sub_list)
            binned_sub_p[bin] = [mean_class, mean_class, mean_class, len(adj_sub_list)]
'''



######################

print subjectivity_dict['small']
print subjectivity_dict['grey']


with open('4_adjs_stats_exp.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['adj', 'freq', 'sem_class', 'mean dis', 'subjectivity' , 'age', 'p/d'])
    for key, value in new_dict_all_adjs_d.items():
        if key in subjectivity_dict.keys():
            writer.writerow([key, value[0], value[1], interim_mean_cd[key], subjectivity_dict[key], '4', 'child-directed'])
    for key, value in new_dict_all_adjs_p.items():
        if key in subjectivity_dict.keys():
            writer.writerow([key, value[0], value[1], interim_mean_cp[key], subjectivity_dict[key], '4', 'child-produced'])

#for input freq p2exp, need # total multi adj strings and need if adj was in second position (adj_seq_list[d or p])
#le', 'fun'], ['red', 'nice'], ['red', 'little'], ['red', 'bright'], ['little', 'naughty'], ['big', 'nice'], ['little', 'grease'], ['podgy', 'old'], ['little', 'horrible'], ['weensie', 'eensie'], ['little', 'laze'], ['little', 'fun'], ['bad', 'big'], ['little', 'poor'], ['old', 'nasty'], ['big', 'great'], ['slop', 'nice']]

with open('4_class_stats_exp.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['class', 'mean', 'CI1', 'CI2', 'N', 'age','p/d'])
    for key, value in semanticClassDict_d.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '4','child-directed'])
    for key, value in semanticClassDict_p.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], '4','child-produced'])
    #for key, value in semanticClassDict_d_binned.items():
        #writer.writerow([key, value[0], value[1], value[2], value[3], 'child-directed, 2-4, binned'])
    #for key, value in semanticClassDict_p_binned.items():
        #writer.writerow([key, value[0], value[1], value[2], value[3], 'child-produced, 2-4, binned'])

outfile_diff_adjs = open("diff_adjs_2.txt", 'w')
diff_adjs = {}
outfile_diff_adjs.write('child-produced 2-4:\n')
for adj in old_c_p_dict.keys():
    if adj not in subjectivity_dict.keys():
        outfile_diff_adjs.write(adj+'\t'+str(len(old_c_p_dict[adj]))+'\n')
        if adj not in diff_adjs.keys():
            diff_adjs[adj] = len(old_c_p_dict[adj])
        else:
            old_count = diff_adjs[adj]
            diff_adjs[adj] = old_count + len(old_c_p_dict[adj])

outfile_diff_adjs.write('child-directed 2-4:\n')
for adj in old_c_d_dict.keys():
    if adj not in subjectivity_dict.keys():
        outfile_diff_adjs.write(adj + '\t' + str(len(old_c_d_dict[adj]))+'\n')
        if adj not in diff_adjs.keys():
            diff_adjs[adj] = len(old_c_d_dict[adj])
        else:
            old_count = diff_adjs[adj]
            diff_adjs[adj] = old_count + len(old_c_d_dict[adj])

sorted_diff = OrderedDict(sorted(diff_adjs.iteritems(), key=lambda (k,v):(v,k), reverse=True))

outfile_diff_all = open('all_diff_adjs_2.txt', 'w')
for x in sorted_diff.keys():
    outfile_diff_all.write(x + '\t'+str(sorted_diff[x]))
    outfile_diff_all.write('\n')


open_mind_classes = {"nationality":0, "material": 1, "shape":2, "color":3,"temporal":4,
                                "location":5, "human":6,"age":7, "physical":8,"speed":9, "dimension":10, "value":11, "other":12}


#when shape-nationaliaty-material are all the same (0.0), just make them one category, need to figure out how to combine
new_semanticClassDict_p = {}
new_semanticClassDict_d = {}
Sem_Dict_p = {}
Sem_Dict_d = {}
checked_classes_d = []
checked_classes_p = []

open_mind_list = ["nationality", "material", "shape", "color","temporal",
                                "location", "human","age", "physical","speed", "dimension","value", "other"]


class_pos_d = {}
class_pos_p = {}
count_p = 0
count_d = 0
for x in open_mind_list:
    class_pos_d[x] = count_d
    count_d += 1

#class_pos_d['other'] = 100

for x in open_mind_list:
    class_pos_p[x] = count_p
    count_p += 1
#class_pos_p['other'] = 100
print semanticClassDict_d['nationality'], "nationality"
#print 'grey: ',subjectivity_dict['grey'], ' gray: ', subjectivity_dict['gray']
#print class_pos_d

#print new_dict_all_adjs_p, "look for dis"
p2exp_d = {} #N: numb of adj strings that contained adj, and f the freq adj was in second position, frequency, by classes, [by binned],
B_L = []
test_B_L = []
sub_pos_dict = {}
sub_count = 0



#binned_sub_d_12_dict

sort_keys = sorted(binned_sub_d12.keys())
for num in sort_keys:
    test_B_L.append(binned_sub_d12[num][3])
    sub_pos_dict[num] = sub_count
    sub_count += 1
#print sub_pos, "breaak" working! yay
#print adj_sub_bin_d
print test_B_L #use for 3-way testings as well as 2 way
#NEW_DICT_ALL_ADJS_D {'cute': [22, 'other']
#getting all tokens in bins into big list
for name in open_mind_list:
    name_count = 0
    for x in interim_new_dict_all_adjs_d.keys():
        if interim_new_dict_all_adjs_d[x][1] in name.split('/'):
            name_count += interim_new_dict_all_adjs_d[x][0]
    B_L.append(name_count)
print B_L




#B_L_binned = [B_L[0], sum(B_L[1:4]), sum(B_L[4:])]
#subjectivity dict = {adj: score, adj tokens} or wait, arrange by score
#sort by subjectivity, {score: num tokes in score)
#for adj in new
num_multistrings_d = len(adj_seq_list_d)

#print subjectivity_dict['beautiful']
#print sub_dict_d[0.935714285714286]
#print new_dict_all_adjs_d['beautiful']
#this has all the smoothing and no dup stuff
V = len(interim_new_dict_all_adjs_d.keys())
L = .5
D = L * V
total_tokes = sum(B_L)
#print sub_dict_d
#print B_L
for adj in interim_new_dict_all_adjs_d:  #goes 1away, 2away
    if adj in subjectivity_dict.keys():
        p2s = []
        count = 0 #f
        total_count = 0 #N
        #print adj, "ADJ"
        for stri in adj_seq_list_d:
            #print stri[1]
            if adj == stri[1]:
                count += 1
            if adj in stri:
                total_count += 1
            #if adj in stri[1] or adj in stri[0]:
                #total_count += 1
        #print count
        p2s.append(total_count)
        p2s.append(count)
        p2s.append(float((count + L) / (total_count + 2*L)))  # p2s.append(float(count / num_multistrings_p)) #input freq baseline
        #p2exp_d[adj] = [p2_in_feq]
        class_actual = new_dict_all_adjs_d[adj][1]
        class_maybe = ''
        for this_class in open_mind_list:
            if class_actual in this_class.split('/'):
                class_maybe = this_class
        #pos = open_mind_classes[class_maybe]
        bin_class = adj_sub_bin_d_dict[adj]
        bin_pos = sub_pos_dict[bin_class]
        pos = class_pos_p[class_maybe]
        sub_pos = subjectivity_dict[adj]
        #pos_bin = binned_class_pos[new_dict_all_adjs_d[adj][1]]
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if dup_or_not == 'n':
            bin_less_than = sum(test_B_L[:bin_pos])
            bin_equal_than = test_B_L[bin_pos] - interim_new_dict_all_adjs_d[adj][0]
            less_than = sum(B_L[:pos])
            equal_than = B_L[pos] - interim_new_dict_all_adjs_d[adj][0]
            sub_less_than = point1sub_d[adj][0]#sub_dict_d[sub_pos][1]
            sub_equal_than = point1sub_d[adj][1] - (interim_new_dict_all_adjs_d[adj][0]-1)#sub_dict_d[sub_pos][0] - (interim_new_dict_all_adjs_d[adj][0]-1)
            new_total_tokes = total_tokes - (interim_new_dict_all_adjs_d[adj][0]-1) + D
            exp = (less_than + (0.5 * equal_than)+L) / new_total_tokes
            sub_exp = (sub_less_than + (0.5 * sub_equal_than)+L) / new_total_tokes
            bin_exp = (bin_less_than + (0.5 * bin_equal_than)+L)/ new_total_tokes
            #print sub_less_than, sub_equal_than, sub_exp
        else:
            less_than = sum(B_L[:pos])
            equal_than = B_L[pos]
            sub_less_than = sub_dict_d[sub_pos][1]
            sub_equal_than = sub_dict_d[sub_pos][0]
            exp = (less_than + 0.5*equal_than + L)/(total_tokes + D)
            sub_exp = (sub_less_than + (0.5*sub_equal_than) + L)/(total_tokes + D)
        #binned_less_than = sum(B_L_binned[:pos_bin])
        #binned_equal_than = B_L_binned[pos_bin]
        #binned_exp = (binned_less_than + 0.5*binned_equal_than)/total_tokes
        p2s.append(exp)
        p2s.append(sub_exp)
        p2s.append(bin_exp)
        #p2s.append(binned_exp)
        p2exp_d[adj] = p2s

#print sub_dict_d
p2exp_p = {}
B_L_p = []

#print p2exp_d['small']
#print p2exp_p['small']


for name in open_mind_list:
    name_count = 0
    for x in interim_new_dict_all_adjs_p.keys():
        if interim_new_dict_all_adjs_p[x][1] in name.split('/'):
            name_count += interim_new_dict_all_adjs_p[x][0]
    B_L_p.append(name_count)

#print sum(B_L_p)

#B_L_binned_p = [B_L_p[0], sum(B_L_p[1:4]), sum(B_L_p[4:])]
num_multistrings_p = len(adj_seq_list_p)

total_tokes = sum(B_L_p)

#if dup_or_not == 'n', then need to get rid of counts of certain adj

for adj in interim_new_dict_all_adjs_p: #goes 1away, 2away
    if adj in subjectivity_dict.keys():# and new_dict_all_adjs_p[adj][1] != 'other':
        p2s = []
        count = 0 #f
        total_count = 0 #N
        #print adj, "ADJ"
        for stri in adj_seq_list_p:
            if adj == stri[1]:
                count += 1
            if adj in stri:
                total_count += 1
        #print count
        p2s.append(total_count)
        p2s.append(count)
        p2s.append(float((count + L)/ (total_count+D)))  # p2s.append(float(count / num_multistrings_p)) #input freq baseline
        #p2exp_p[adj] = [p2_in_feq]
        class_actual = interim_new_dict_all_adjs_p[adj][1]
        class_maybe = ''
        for this_class in open_mind_classes:
            if class_actual in this_class.split('/'):
                class_maybe = this_class
        pos = class_pos_p[class_maybe]
        sub_pos = subjectivity_dict[adj]
        #pos_bin = binned_class_pos[new_pict_all_adjs_p[adj][1]]
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if dup_or_not == 'n':
            less_than = sum(B_L_p[:pos])
            equal_than = B_L_p[pos] - interim_new_dict_all_adjs_p[adj][0]
            sub_less_than = sub_dict_p[sub_pos][1]
            sub_equal_than = sub_dict_p[sub_pos][0] - interim_new_dict_all_adjs_p[adj][0]
            new_total_tokes = total_tokes - interim_new_dict_all_adjs_p[adj][0]
            exp = (less_than + 0.5 * equal_than) / new_total_tokes
            sub_exp = (sub_less_than + 0.5 * sub_equal_than) / new_total_tokes
        else:
            less_than = sum(B_L_p[:pos])
            equal_than = B_L_p[pos]
            sub_less_than = sub_dict_p[sub_pos][1]
            sub_equal_than = sub_dict_p[sub_pos][0]
            new_total_tokes = total_tokes - new_dict_all_adjs_d[adj][0]
            exp = (less_than + 0.5 * equal_than) / new_total_tokes
            sub_exp = (sub_less_than + 0.5 * sub_equal_than) / new_total_tokes
        #binned_less_than = sum(B_L_binned[:pos_bin])
        #binned_equal_than = B_L_binned[pos_bin]
        #binned_exp = (binned_less_than + 0.5*binned_equal_than)/total_tokes
        #print pos,adj,new_dict_all_adjs_p[adj], exp, less_than, equal_than, sub_exp, sub_less_than, sub_equal_than
        p2s.append(exp)
        p2s.append(sub_exp)
        #p2s.append(binned_exp)
        p2exp_p[adj] = p2s

#print p2exp_d['second']
#print p2exp_p['wee']#, p2exp_p['right']
#print p2exp_d['wee'], p2exp_d['right']

#hyp1 = input baseline, hyp2 = lexical class, hyp3 = subjectivity

#do only the intersection of the adjs at first. p2exp is based on input, p(D|H) is based on output
#the baseline needs to be based on output
#need to create new dictionary between p and d.  all the info of d, but with the N and f and p2exp baseline of p

#####################
'''
interim_p2exp = {}

V = len(new_dict_all_adjs_d.keys())
L = .5
D = L * V
interim_total_tokes = 0
for x in interim_new_dict_all_adjs_d.keys():
    interim_total_tokes += interim_new_dict_all_adjs_d[x][0]

for adj in interim_new_dict_all_adjs_p:  #goes 1away, 2away
    if adj in subjectivity_dict.keys():
        p2s = []
        count = 0 #f
        total_count = 0 #N
        p_count = 0
        t_count = 0
        #print adj, "ADJ"
        for stri in final_adj_list_d:
            #print stri[1]
            if adj == stri[1]:
                count += 1
            if adj in stri:
                total_count += 1
            #if adj in stri[1] or adj in stri[0]:
                #total_count += 1
        for stri in final_adj_list_p:
            if adj == stri[1]:
                p_count += 1
            if adj in stri:
                t_count += 1
        #print count
        p2s.append(t_count)
        p2s.append(p_count)
        if adj in interim_new_dict_all_adjs_d:
            p2s.append(float((count + L) / (total_count + 2*L)))  # p2s.append(float(count / num_multistrings_p)) #input freq baseline
            #p2exp_d[adj] = [p2_in_feq]
            #class_actual = new_dict_all_adjs_p[adj][1]
            #class_maybe = ''
            #for this_class in open_mind_list:
                #if class_actual in this_class.split('/'):
                    #class_maybe = this_class
            #pos = open_mind_classes[class_maybe]
            ##sub_bin_class = adj_sub_bin_d_dict[adj]  # adj_sub_bin_d[adj] = bin
            ##pos = sub_pos_dict[sub_bin_class]
            sub_pos = subjectivity_dict[adj]
            #pos_bin = binned_class_pos[new_dict_all_adjs_d[adj][1]]
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if dup_or_not == 'n':
                less_than = sum(test_B_L[:pos])
                equal_than = test_B_L[pos] - interim_new_dict_all_adjs_p[adj][0]
                sub_less_than = point1sub_d[adj][0]
                sub_equal_than = point1sub_d[adj][1] - (interim_new_dict_all_adjs_d[adj][0]-1)
                new_total_tokes = interim_total_tokes - (interim_new_dict_all_adjs_d[adj][0]-1) + D
                exp = (less_than + (0.5 * equal_than)+L) / new_total_tokes
                sub_exp = (sub_less_than + (0.5 * sub_equal_than)+L) / new_total_tokes
                #print sub_less_than, sub_equal_than, sub_exp
            else:
                #less_than = sum(B_L[:pos])
                #equal_than = B_L[pos]
                sub_less_than = point1sub_d[adj][0]
                sub_equal_than = point1sub_d[adj][1]
                #exp = (less_than + 0.5*equal_than + L)/(total_tokes + D)
                sub_exp = (sub_less_than + (0.5*sub_equal_than) + L)/(total_tokes + D)
            #binned_less_than = sum(B_L_binned[:pos_bin])
            #binned_equal_than = B_L_binned[pos_bin]
            #binned_exp = (binned_less_than + 0.5*binned_equal_than)/total_tokes
            p2s.append(exp)
            p2s.append(sub_exp)
            #p2s.append(binned_exp)
            interim_p2exp[adj] = p2s
        else:
            p2s.append(0.5)
            p2s.append(0.5)
            p2s.append(0.5)
            interim_p2exp[adj] = p2s

#print interim_p2exp
'''
####################

new_p2exp = {}

for adj in p2exp_p.keys():
    if adj in p2exp_d.keys():
        new_value = [p2exp_p[adj][0], p2exp_p[adj][1], p2exp_d[adj][2], p2exp_d[adj][3], p2exp_d[adj][4], p2exp_d[adj][5]]
        #print p2exp_d[adj][5]
        new_p2exp[adj] = new_value
    else:
        new_value = [p2exp_p[adj][0], p2exp_p[adj][1], 0.5, 0.5, 0.5, 0.5]
        new_p2exp[adj] = new_value

print new_p2exp

'''
interim_log_sum_hyp1 = 0
for adj in interim_p2exp:
    #log_sum = 0
    N = interim_p2exp[adj][0]
    f = interim_p2exp[adj][1]
    p2exp = interim_p2exp[adj][2]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    if pDadj_H == 0:
        #pDadj_H = 10**-323
        print pDadj_H, p2exp, N, f, adj
    interim_log_sum_hyp1 += np.log(pDadj_H)

interim_log_sum_hyp2 = 0
for adj in interim_p2exp:
    #log_sum = 0
    N = interim_p2exp[adj][0]
    f = interim_p2exp[adj][1]
    p2exp = interim_p2exp[adj][3]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #print pDadj_H, p2exp, N, f, adj
    interim_log_sum_hyp2 += np.log(pDadj_H)

interim_log_sum_hyp3 = 0
for adj in interim_p2exp:
    #log_sum = 0
    N = interim_p2exp[adj][0]
    f = interim_p2exp[adj][1]
    p2exp = interim_p2exp[adj][4]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #print pDadj_H, p2exp, N, f, adj
    interim_log_sum_hyp3 += np.log(pDadj_H)

print interim_log_sum_hyp1, interim_log_sum_hyp2, interim_log_sum_hyp3
sample_bf = np.e**(interim_log_sum_hyp1-interim_log_sum_hyp2)#log_sum_hyp1/log_sum_hyp2#(np.e**log_sum_hyp1)/(np.e**log_sum_hyp2)
sample_bf2 = np.e**(interim_log_sum_hyp2-interim_log_sum_hyp3)#log_sum_hyp2/log_sum_hyp3
sample_bf3 = np.e**(interim_log_sum_hyp1-interim_log_sum_hyp3)#log_sum_hyp1/log_sum_hyp3

print sample_bf
print sample_bf2
print sample_bf3

'''
adj_analysis_table = {} #key: adj, value: freq, lexical class, subjectivity, p2_exp, p(D|H1), p(D|H2), p(D|H3)

log_sum_hyp1 = 0
for adj in new_p2exp:
    #log_sum = 0
    N = new_p2exp[adj][0]
    f = new_p2exp[adj][1]
    p2exp = new_p2exp[adj][2]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #if adj not in adj_analysis_table.keys():
        #adj_analysis_table[adj] = [interim_new_dict_all_adjs_d[adj][0], interim_new_dict_all_adjs_d[adj][1] ]
    if pDadj_H == 0:
        #pDadj_H = 10**-323
        print pDadj_H, p2exp, N, f, adj
    log_sum_hyp1 += np.log(pDadj_H)


log_sum_hyp2 = 0
for adj in new_p2exp:
    #log_sum = 0
    N = new_p2exp[adj][0]
    f = new_p2exp[adj][1]
    p2exp = new_p2exp[adj][3]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #if pDadj_H == 0:
        #pDadj_H = 10**-323
    log_sum_hyp2 += np.log(pDadj_H)


log_sum_hyp3 = 0
for adj in new_p2exp:
    N = new_p2exp[adj][0]
    f = new_p2exp[adj][1]
    p2exp = new_p2exp[adj][4]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #if pDadj_H == 0:
        #pDadj_H = 10**-323
    log_sum_hyp3 += np.log(pDadj_H)

log_sum_hyp4 = 0
for adj in new_p2exp:
    N = new_p2exp[adj][0]
    f = new_p2exp[adj][1]
    p2exp = new_p2exp[adj][5]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    #if pDadj_H == 0:
        #pDadj_H = 10**-323
    log_sum_hyp4 += np.log(pDadj_H)


print log_sum_hyp1, log_sum_hyp2, log_sum_hyp3, log_sum_hyp4
sample_bf = np.e**(log_sum_hyp1-log_sum_hyp2)#log_sum_hyp1/log_sum_hyp2#(np.e**log_sum_hyp1)/(np.e**log_sum_hyp2)
sample_bf2 = np.e**(log_sum_hyp2-log_sum_hyp3)#log_sum_hyp2/log_sum_hyp3
sample_bf3 = np.e**(log_sum_hyp1-log_sum_hyp3)#log_sum_hyp1/log_sum_hyp3



#print sample_bf, 'directed hyp1/hyp2'
#print sample_bf2, 'directed hyp2/hyp3'
#print sample_bf3, 'directed hyp1/hyp3'

sys.exit()

log_sum_hyp1_p = 0
for adj in p2exp_p:
    #log_sum = 0
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][2]
    pDadj_H = scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    if pDadj_H == 0:
        pDadj_H = 10**-323
    log_sum_hyp1_p += np.log(pDadj_H)

log_sum_hyp2_p = 0
for adj in p2exp_p:
    #log_sum = 0
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][3]
    pDadj_H = scipy.special.binom(N,f)* (p2exp ** f) * ((1 - p2exp) ** (N - f))
    if pDadj_H == 0:
        pDadj_H = 10**-323
    log_sum_hyp2_p += np.log(pDadj_H)


log_sum_hyp3_p = 0
for adj in p2exp_p:
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][4]
    pDadj_H =scipy.special.binom(N,f) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    if pDadj_H == 0:
        pDadj_H = 10**-323
    log_sum_hyp3_p += np.log(pDadj_H)


print log_sum_hyp1_p, log_sum_hyp2_p, log_sum_hyp3_p
sample_bf_p = np.e**(log_sum_hyp1_p-log_sum_hyp2_p)#(np.e**log_sum_hyp1)/(np.e**log_sum_hyp2)
sample_bf2_p = np.e**(log_sum_hyp2_p-log_sum_hyp3_p)
sample_bf3_p = np.e**(log_sum_hyp1_p-log_sum_hyp3_p)


print sample_bf_p, 'produced hyp1/hyp2'
print sample_bf2_p, 'produced hyp2/hyp3'
print sample_bf3_p, 'produced hyp1/hyp3'
