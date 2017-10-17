#!/usr/bin/python

import re
import os
#import itertools
#from itertools import groupby
#import sys
#import csv
#import numpy as np
#import matplotlib.pyplot as plt

outfile = open('HSLLD_ages.txt', 'w')

#go

rootdir = os.getcwd()

for file_folder in os.walk(rootdir):  # just want to look at the .cha files
# for new_folder in file_folder:
#        print "first folder", new_folder
#        for new_new_folder in new_folder:
#            print "second folder" ,new_new_folder
    for filename in file_folder:
        print "filename", filename
        if '.cha' in filename:
            infile = open(filename, 'r')

            readinfile = infile.read()

            infile.close()

            x = re.findall(r'CHI\|(.+?)\|', readinfile)

            # if x is more than one, will be list and not str, need to adjust in outfile.write

            outfile.write(filename + "\t" + x + '\n')
