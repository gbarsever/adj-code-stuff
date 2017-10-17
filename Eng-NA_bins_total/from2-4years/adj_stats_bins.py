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
import operator
from scipy.special import comb #comb(N,k, exact=False)


#CIs = bootstrap.ci(data=x,statfunction= scipy.mean) #x is the dataset (nsamples = 10,000), 95%

# want to track mean distance from noun of all adjectives
# so first make all files in to a list of lists(which will be sentences, split by whitespace)
# postition of noun-position of adj
# dictionary of adjs with values as the position
# take average


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



all_da_utts = []
c_directed = []
c_produced = []
#dict = {'cats':['tiger','leopards','jaguars'], 'dogs': [...]}

d_all_rough = []
p_all_rough = []
dup_or_not = raw_input("include duplicate adjs? (e.g. \'wee wee wee kitty\'. enter y for yes or n for no\n")
binned_or_not = raw_input("use binned classes?\n")
#folder = raw_input("pick a folder: Eng-NA or Eng-UK")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f[0] == '+':
        infile = open(f, 'r')
        reading = infile.read()
        rough = re.findall(r'%mor:.+\.',reading,re.MULTILINE)
        rough2 = re.findall(r'%mor:.+\?',reading,re.MULTILINE)
        rough3 = re.findall(r'%mor:.+!',reading,re.MULTILINE)
        if rough != []:
            p_all_rough.append(rough) #changed from append
        if rough2 != []:
            p_all_rough.append(rough2)
        if rough3 != []:
            p_all_rough.append(rough3)
        #rough = re.findall(r'%mor:.+\.|\?|!', reading, re.MULTILINE)
        #p_all_rough.extend(rough) #changed from append

    elif f[0] == '-':
        infile = open(f, 'r')
        reading = infile.read()
        rough = re.findall(r'%mor:.+\.',reading,re.MULTILINE)
        rough2 = re.findall(r'%mor:.+\?',reading,re.MULTILINE)
        rough3 = re.findall(r'%mor:.+!',reading,re.MULTILINE)
        if rough != []:
            d_all_rough.append(rough) #changed from append
        if rough2 != []:
            d_all_rough.append(rough2)
        if rough3 != []:
            d_all_rough.append(rough3)
#print d_all_rough[0:20]

                #split_thing = thing.split()
                #c_directed.append(split_thing)
                #all_da_utts.append(split_thing)
        #all_mor = re.findall(r'mor:.+\.|\?|\!?', readinfile)

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
    print sentence
    for word2 in sentence:
        print word2
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

new_adj_seq_list_d = []
for strang in adj_seq_list_d:
    if len(strang) == 2:
        new_adj_seq_list_d.append(strang)
    else:
        new_adj_seq_list_d.append([strang[0],strang[1]])

adj_seq_list_d = new_adj_seq_list_d


for adj_seq in adj_seq_list_d:
    for word in set(adj_seq):
        if word in c_d_dict:
            temp = c_d_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            c_d_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]



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


for adj_seq in adj_seq_list_p:
    for word in set(adj_seq):
        if word in c_p_dict:
            temp = c_p_dict[word]
            temp.extend([i for i,val in enumerate(adj_seq) if val==word])
        else:
            c_p_dict[word] = [i for i,val in enumerate(adj_seq) if val==word]



#need actual size of corpus used
#flag for include reduplication, not include....


list_adjs_paper = [['old','new','rotten','fresh'],['red','yellow','green',
                   'blue','purple','brown'],['wooden','plastic','metal'],['good',
                   'bad'],['round','square'],['big','small','huge','tiny','short',
                   'long'],['smooth','hard','soft']]

print "# adjs in produced: ", len(c_p_dict)
print "# adjs in directed: ", len(c_d_dict)

#~~~~~~~~~~~~~~~~~
list_adjs_p = sorted(c_p_dict, key=lambda k: len(c_p_dict[k]), reverse=True)
list_adjs_d = sorted(c_d_dict, key=lambda k: len(c_d_dict[k]), reverse=True)

print "age 3 adj-seq directed", len(adj_seq_list_d)
print "age 3 adj-seq produced", len(adj_seq_list_p)
print "age 3 # adj types directed", len(list_adjs_d)
print "age 3 # adj types produced", len(list_adjs_p)



for utt in c_directed:
    for wordpair in utt:
        if "spin" in wordpair or "fleece" in wordpair or "puff" in wordpair or "thirst" in wordpair or "crust" in wordpair:
            print utt

for utt in c_produced:
    for wordpair in utt:
        if "spin" in wordpair or "fleece" in wordpair or "puff" in wordpair or "thirst" in wordpair or "crust" in wordpair:
            print utt

outfile_adjs = open('2-4adjs.txt', 'w')
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

for x in list_adjs_d:
    for y in new_d:
        if x in y:
            sem_label = y[0]
    new_dict_all_adjs_d[x] = [len(c_d_dict[x]), sem_label]

for x in list_adjs_p:
    for y in new_p:
        if x in y:
            sem_label = y[0]
    new_dict_all_adjs_p[x] = [len(c_p_dict[x]), sem_label]
#print new_dict_all_adjs_p
with open('2-4_adjsstats.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['adj', 'freq', 'sem_class', 'p/d'])
    for key, value in new_dict_all_adjs_d.items():
        writer.writerow([key, value[0], value[1], 'child-directed'])
    for key, value in new_dict_all_adjs_p.items():
        writer.writerow([key, value[0], value[1], 'child-produced'])

print "NEW_DICT_ALL_ADJS_D", new_dict_all_adjs_d
#~~~~~~~~~~~~~~~~~~~~

mean_cd = dict()
mean_cp = dict()
for adj in c_d_dict:
    mean_cd[adj] = sum(c_d_dict[adj]) / float(len(c_d_dict[adj]))
for adj in c_p_dict.keys():
    mean_cp[adj] = sum(c_p_dict[adj]) / float(len(c_p_dict[adj]))

#print mean_cd
#to get 95% confidence intervals, need raw data from each word together to be resampled? not just means of words in category to be resampled?
'''
sem_class_list = []
for sem_class in list_adjs_paper:
    temp = []
    for word in sem_class:
        if word in mean_cp:
            temp.append(mean_cp[word])
        else:
            print word, "not in mean_cp"
    sem_class_list.append(temp)


mean_sem_class_list = []
for thing in sem_class_list:
    mean_sem_class_list.append(sum(thing) / float(len(thing)))

print "from paper: produced ", mean_sem_class_list

'''
c3 = [val for val in c_p_dict.keys() if val in c_d_dict.keys()]
#print(c3)
#print(len(c3)) #this is length of the overlap

binned_classes = [['value'],['dimension', 'age', 'physical'],['shape', 'color', 'material']] #value, dimension age physical, shape color material (with other plot for color maybe)
#print all_adjs
semanticClassDict_p = dict()  # key is class (which is the first element of list, value is average and CIs
for semanticclass in all_adjs:
    #print semanticclass
    semanticclasslist_p = []
    if semanticclass[0] != 'other':  #get rid of other category
        for word in semanticclass[1:]:
            if word in c_p_dict:
                semanticclasslist_p.extend(c_p_dict[word])
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

#print semanticClassDict_p, "look for p"

semanticClassDict_d = dict() #key is class (which is the first element of list, value is average
for semanticclass in all_adjs:
    semanticclasslist = []
    if semanticclass[0] != 'other':  #get rid of other category
        for word in semanticclass[1:]:
            if word in c_d_dict:
                semanticclasslist.extend(c_d_dict[word])
    if semanticclasslist != []:
        if len(set(semanticclasslist)) != 1:
            #bootstrap.ci doesnt like it when there is only 1 unique element in dataset
            CIs = bootstrap.ci(data=semanticclasslist, statfunction=scipy.mean)
            mean_class = scipy.mean(semanticclasslist)
            semanticClassDict_d[semanticclass[0]] = [mean_class, CIs[0], CIs[1], len(semanticclasslist)]
        else:
            mean_class = scipy.mean(semanticclasslist)
            semanticClassDict_d[semanticclass[0]] = [mean_class, mean_class, mean_class, len(semanticclasslist)]


sys.exit()
semanticClassDict_d_binned = dict()
semanticClassDict_p_binned = dict()
for bin in binned_classes:
    binned_list_d = []
    binned_list_p = []
    key = "-".join(bin)
    for thing in bin:
        for semanticclass in all_adjs:
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
    for sem_class in all_adjs:
        if adj in sem_class[1:]:
            adj_class_dict_d[adj] = sem_class[0]

for adj in c_p_dict.keys():
    for sem_class in all_adjs:
        if adj in sem_class[1:]:
            adj_class_dict_p[adj] = sem_class[0]

#print c_p_dict['slime'], "SLIEE"

flat_ex1 = [item for sublist in list_adjs_paper for item in sublist]

flat_list = [item for sublist in all_adjs for item in sublist]
for x in mean_cp.keys():
    if x not in flat_list:
        print x
print "^^^"
for x in mean_cd.keys():
    if x not in flat_list:
        print x
print "^^^"
'''
added:

tough
wobble
frost
rowdy
^^^
crust
bird
wobble
shiver
chatter
fleece
stripe
^^^

soggy
flap
ordinary
^^^
soggy
true
lonely
rose
important
use
sleeved
flap
spin
straight
^^^
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
classes = ['value','dimension', 'age', 'physical','shape', 'color', 'material']
class_pos = {'value':0,'dimension':1, 'age':2, 'physical':3,'shape':4, 'color':5, 'material':6, 'other':100}
binned_class_pos = {'value':0,'dimension':1, 'age':1, 'physical':1,'shape':2, 'color':2, 'material':2, 'other':100}

#read in subjectivity results (also make everything lowercase)
subjectivity_dict = {}
subjectivity_dict_av = {}
with open('SDG_subjectivity-expanded_results_copy.csv', 'rU') as csvfile: #4th column adj, 6th column response (need to be averaged)
    reader = csv.DictReader(csvfile)
    for element in reader:
        adj = element['predicate'].lower()
        if adj not in subjectivity_dict.keys():
            subjectivity_dict[adj] = [float(element['response'])]
        else:
            temp = subjectivity_dict[adj]
            temp = temp.append(float(element['response']))

for adj in subjectivity_dict.keys():
    subjectivity_dict_av[adj] = sum(subjectivity_dict[adj])/len(subjectivity_dict[adj])

sorted_x = sorted(subjectivity_dict_av, key=subjectivity_dict_av.get, reverse=True)
print sorted_x

p2exp_d = {} #N: numb of adj strings that contained adj, and f the freq adj was in second position, frequency, by classes, [by binned],
B_L = []

#NEW_DICT_ALL_ADJS_D {'cute': [22, 'other']
#getting all tokens in bins into big list
for name in classes:
    name_count = 0
    for x in new_dict_all_adjs_d.keys():
        if new_dict_all_adjs_d[x][1] == name:
            name_count += new_dict_all_adjs_d[x][0]
    B_L.append(name_count)

B_L_binned = [B_L[0], sum(B_L[1:4]), sum(B_L[4:])]
#subjectivity dict = {adj: score} or wait, arrange by score
#sort by subjectivity, {score: num tokes)
#for adj in new
num_multistrings_d = len(adj_seq_list_d)

total_tokes = sum(B_L)
for adj in new_dict_all_adjs_d:
    p2s = []
    count = 0 #f
    total_count = 0 #N
    #print adj, "ADJ"
    for stri in adj_seq_list_d:
        #print stri[1]
        if adj in stri[1]:
            count += 1
        if adj in stri[1] or adj in stri[0]:
            total_count += 1
    #print count
    p2s.append(total_count)
    p2s.append(count)
    p2s.append(float(count / total_count))  # p2s.append(float(count / num_multistrings_p)) #input freq baseline
    #p2exp_d[adj] = [p2_in_feq]
    pos = class_pos[new_dict_all_adjs_d[adj][1]]
    pos_bin = binned_class_pos[new_dict_all_adjs_d[adj][1]]
    if pos != 100:
        less_than = sum(B_L[:pos])
        equal_than = B_L[pos]
        binned_less_than = sum(B_L_binned[:pos_bin])
        binned_equal_than = B_L_binned[pos_bin]
        binned_exp = (binned_less_than + 0.5*binned_equal_than)/total_tokes
        exp = (less_than + 0.5*equal_than)/total_tokes
        p2s.append(exp)
        p2s.append(binned_exp)
        p2exp_d[adj] = p2s


p2exp_p = {}
B_L_p = []

for name in classes:
    name_count = 0
    for x in new_dict_all_adjs_p.keys():
        if new_dict_all_adjs_p[x][1] == name:
            name_count += new_dict_all_adjs_p[x][0]
    B_L_p.append(name_count)

#print B_L
B_L_binned_p = [B_L_p[0], sum(B_L_p[1:4]), sum(B_L_p[4:])]
num_multistrings_p = len(adj_seq_list_p)

total_tokes = sum(B_L_p)
for adj in new_dict_all_adjs_p:
    p2s = []
    count = 0 #f2(adjx)
    total_count = 0 #N(adjx)
    #print adj, "ADJ"
    for stri in adj_seq_list_p:
        #print stri[1]
        if adj in stri[1]:
            count += 1
        if adj in stri[1] or adj in stri[0]:
            total_count += 1
    #print count
    p2s.append(total_count)
    p2s.append(count)
    p2s.append(float(count / total_count))#p2s.append(float(count / num_multistrings_p)) #input freq baseline
    #p2exp_d[adj] = [p2_in_feq]
    pos = class_pos[new_dict_all_adjs_p[adj][1]]
    pos_bin = binned_class_pos[new_dict_all_adjs_p[adj][1]]
    if pos != 100:
        less_than = sum(B_L_p[:pos])
        equal_than = B_L_p[pos]
        binned_less_than = sum(B_L_binned_p[:pos_bin])
        binned_equal_than = B_L_binned_p[pos_bin]
        binned_exp = (binned_less_than + 0.5*binned_equal_than)/total_tokes
        exp = (less_than + 0.5*equal_than)/total_tokes
        p2s.append(exp) #lexical classes
        p2s.append(binned_exp) #binned classes
        p2exp_p[adj] = p2s


print p2exp_p

log_sum_hyp1 = 0
for adj in p2exp_d:
    #log_sum = 0
    N = p2exp_d[adj][0]
    f = p2exp_d[adj][1]
    p2exp = p2exp_d[adj][2]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp1 += np.log(pDadj_H)

log_sum_hyp2 = 0
for adj in p2exp_d:
    #log_sum = 0
    N = p2exp_d[adj][0]
    f = p2exp_d[adj][1]
    p2exp = p2exp_d[adj][3]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp2 += np.log(pDadj_H)


log_sum_hyp3 = 0
for adj in p2exp_d:
    N = p2exp_d[adj][0]
    f = p2exp_d[adj][1]
    p2exp = p2exp_d[adj][4]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp3 += np.log(pDadj_H)
'''
log_sum_hyp4 = 0
for adj in p2exp_d:
    N = big_adj_dict[adj][0]
    f = big_adj_dict[adj][1]
    p2exp = big_adj_dict[adj][5]
    pDadj_H = comb(N, f) * p2exp ^ f * (1 - p2exp) ^ (N - f)
    log_sum += np.log(pDadj_H)
'''
print log_sum_hyp1, log_sum_hyp2, log_sum_hyp3
sample_bf = np.e**(log_sum_hyp1-log_sum_hyp2)#(np.e**log_sum_hyp1)/(np.e**log_sum_hyp2)
sample_bf2 = np.e**(log_sum_hyp2-log_sum_hyp3)
sample_bf3 = np.e**(log_sum_hyp1-log_sum_hyp3)


print sample_bf, 'directed hyp1/hyp2'
print sample_bf2, 'directed hyp2/hyp3'
print sample_bf3, 'directed hyp1/hyp3'



log_sum_hyp1_p = 0
for adj in p2exp_p:
    #log_sum = 0
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][2]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp1_p += np.log(pDadj_H)

log_sum_hyp2_p = 0
for adj in p2exp_p:
    #log_sum = 0
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][3]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp2_p += np.log(pDadj_H)


log_sum_hyp3_p = 0
for adj in p2exp_p:
    N = p2exp_p[adj][0]
    f = p2exp_p[adj][1]
    p2exp = p2exp_p[adj][4]
    pDadj_H = np.float64(comb(N, f).item()) * (p2exp ** f) * ((1 - p2exp) ** (N - f))
    log_sum_hyp3_p += np.log(pDadj_H)



print log_sum_hyp1_p, log_sum_hyp2_p, log_sum_hyp3_p
sample_bf_p = np.e**(log_sum_hyp1_p-log_sum_hyp2_p)#(np.e**log_sum_hyp1)/(np.e**log_sum_hyp2)
sample_bf2_p = np.e**(log_sum_hyp2_p-log_sum_hyp3_p)
sample_bf3_p = np.e**(log_sum_hyp1_p-log_sum_hyp3_p)


print sample_bf_p, 'produced hyp1/hyp2'
print sample_bf2_p, 'produced hyp2/hyp3'
print sample_bf3_p, 'produced hyp1/hyp3'



sys.exit()


#for input freq p2exp, need # total multi adj strings and need if adj was in second position (adj_seq_list[d or p])
#le', 'fun'], ['red', 'nice'], ['red', 'little'], ['red', 'bright'], ['little', 'naughty'], ['big', 'nice'], ['little', 'grease'], ['podgy', 'old'], ['little', 'horrible'], ['weensie', 'eensie'], ['little', 'laze'], ['little', 'fun'], ['bad', 'big'], ['little', 'poor'], ['old', 'nasty'], ['big', 'great'], ['slop', 'nice']]



big_infile = open('big_list_scontras.txt', 'r')
biginfile = big_infile.readlines()
readbiginfile = []
for c in biginfile:
    readbiginfile.append(c.rstrip())
#print readbiginfile, len(readbiginfile)
with open('4_big_list_additional.csv', 'wb') as big_list:
    writer = csv.writer(big_list)
    writer.writerow(['word','av.distance', 'overlap ex 1','overlap ex 2', 'age', 'child p or d', 'tokens', 'semantic class'])
    for key, value in mean_cd.items():
        tokens = len(c_d_dict[key])
        da_class = adj_class_dict_d[key]
        if key in readbiginfile and key in flat_ex1:
            writer.writerow([key, value, '1', '1', '4','directed', tokens, da_class])
        elif key in readbiginfile and key not in flat_ex1:
            writer.writerow([key, value, '0', '1', '4', 'directed', tokens, da_class])
        elif key not in readbiginfile and key in flat_ex1:
            writer.writerow([key, value, '1', '0', '4', 'directed', tokens, da_class])
        else:
            writer.writerow([key, value, '0', '0', '4', 'directed', tokens, da_class])
    for key, value in mean_cp.items():
        tokens = len(c_p_dict[key])
        da_class = adj_class_dict_p[key]
        if key in readbiginfile and key in flat_ex1:
            writer.writerow([key, value, '1', '1', '4','produced', tokens, da_class])
        elif key in readbiginfile and key not in flat_ex1:
            writer.writerow([key, value, '0', '1', '4', 'produced', tokens, da_class])
        elif key not in readbiginfile and key in flat_ex1:
            writer.writerow([key, value, '1', '0', '4', 'produced', tokens, da_class])
        else:
            writer.writerow([key, value, '0', '0', '4', 'produced', tokens, da_class])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sys.exit()
with open('2-4_twoadjs.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['class', 'mean', 'CI1', 'CI2', 'N', 'label'])
    for key, value in semanticClassDict_d.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], 'child-directed, 2-4, not binned'])
    for key, value in semanticClassDict_p.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], 'child-produced, 2-4, not binned'])
    for key, value in semanticClassDict_d_binned.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], 'child-directed, 2-4, binned'])
    for key, value in semanticClassDict_p_binned.items():
        writer.writerow([key, value[0], value[1], value[2], value[3], 'child-produced, 2-4, binned'])
sys.exit()

if dup_or_not == 'n':
    file_str = 'adj_sem_directed_nodup.csv'
else:
    file_str = 'adj_sem_directed.csv'
    with open(file_str, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in semanticClassDict_d.items():
            writer.writerow([key, value])



if dup_or_not == 'n':
    file_str2 = 'adj_sem_produced_nodup.csv'
else:
    file_str2 = 'adj_sem_produced.csv'
    with open(file_str2, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in semanticClassDict_p.items():
            writer.writerow([key, value])



###################
#~~~~scatter plot try out
#x = semanticClassDict_d.keys()
#y = semanticClassDict_d.values()

#plt.bar(semanticClassDict_d.keys(), semanticClassDict_d.values())
#plt.show()

#plt.bar(range(len(semanticClassDict_p)), semanticClassDict_p.values(), align='center')
#plt.xticks(range(len(semanticClassDict_p)), semanticClassDict_p.keys())
#plt.show()
#N = 50
#x = np.random.rand(N)
#y = np.random.rand(N)
#colors = np.random.rand(N)
#area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radii

#plt.scatter(x, y, s=area, c=colors, alpha=0.5)
#plt.show()


###################
'''
if dup_or_not == 'n':
    outfile_p = open("adjs_produced_UK_NA_nodups.txt", "w")
    outfile_d = open("adjs_directed_UK_NA_nodups.txt", "w")
    outfile_o = open("adjs_overlap_UK_NA_nodups.txt", "w")
else:
    outfile_p = open("adjs_produced_UK_NA.txt", "w")
    outfile_d = open("adjs_directed_UK_NA.txt", "w")
    outfile_o = open("adjs_overlap_UK_NA.txt", "w")

outfile_p.write("Child produced multiple adjs in combined UK and NA corpora\n")
outfile_d.write("Child directed multiple adjs in combined UK and NA corpora\n")
outfile_o.write("Overlap of child directed and produced multiple adjs in combined UK and NA corpora\n")

for x in c_d_dict:
    outfile_d.write(x+"\n")

for x in c_p_dict:
    outfile_p.write(x+"\n")

for x in c3:
    outfile_o.write(x+"\n")

#still need for more than 2 adjs'''

