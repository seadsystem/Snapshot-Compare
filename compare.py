#!/usr/bin/python
# -*- coding: utf-8 -*-
# ============================================================
# File: snapshot.py
# Description: Takes a csv file from the PA1000 and plots all
#              of the Voltage, Current, and Wattage harmonics
#              usage: snapshot.py [source.csv]
# Created by Henry Crute
# 7/30/2014
# ============================================================

import re
import sys
import numpy as np
import matplotlib.pyplot as plt

#finds a string between two strings
def find_between(s, first, last):
   try:
      start = s.index( first ) + len( first )
      end = s.index( last, start )
      return s[start:end]
   except ValueError:
      return ""

#
def normalize_list(word, v_list, a_list, w_list):
   if word.find("mV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' mV')) * 0.001)
   elif word.find("mA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' mA')) * 0.001)
   elif word.find("mW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' mW')) * 0.001)
   elif word.find("μV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' μV')) * 0.000001)
   elif word.find("μA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' μA')) * 0.000001)
   elif word.find("μW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' μW')) * 0.000001)
   elif word.find("nV") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' nV')) * 0.000000001)
   elif word.find("nA") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' nA')) * 0.000000001)
   elif word.find("nW") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' nW')) * 0.000000001)
   elif word.find("V") != -1:
      #print word
      v_list.append(float(find_between(word, ',', ' V')))
      #print "units already normalized"
   elif word.find("A") != -1:
      #print word
      a_list.append(float(find_between(word, ',', ' A')))
      #print "units already normalized"
   elif word.find("W") != -1:
      #print word
      w_list.append(float(find_between(word, ',', ' W')))
      #print "units already normalized"
   else:
      print "none"

#creates a bar graph from a list of numbers with a random color
def bar_graph(shemp_list_in, pa_list_in, title, colorstring, totalPlots, plotNum):
   #normalize shemp_list
   shemp_list = []
   pa_list = []
   max_length = min(len(pa_list_in), len(shemp_list_in))
   max_list = max(shemp_list_in)
   for i in range(max_length):
      shemp_list.append(shemp_list_in[i]/max_list)
   max_list = max(pa_list_in)
   for i in range(max_length):
      pa_list.append(pa_list_in[i]/max_list)

   print shemp_list
   print pa_list

   ind = np.arange(max_length)

   #subplots bar graph   
   plt.subplot(100 + totalPlots * 10 + plotNum)   

   width = .3

   p1 = plt.bar(ind + 0.7, pa_list, width, color=colorstring[0], hold=True)
   p2 = plt.bar(ind + 1, shemp_list, width, color=colorstring[1], hold=True)
   
   plt.ylabel('Normalized Units in Amps')
   plt.title('Harmonics Amplitude of ' + title)
   
   #obtains percent error in error list and assigns the x tick location

   plt.xticks(ind + 1)
   difference = []
   for i in range(len(shemp_list)):
      difference.append(100-100*pa_list[i]/shemp_list[i])
   
   maxY = max(shemp_list)
   plt.yticks(np.arange(-maxY/10, maxY + maxY/10, maxY/6))
   plt.legend((p1[0], p2[0]), ('PA-1000', 'Plug'))

   def percenterr(rects1, rects2):
      #print difference
      # attach text labels
      i = 0
      for rect in rects1:
         height = rect.get_height()
         plt.text(rect.get_x()+rect.get_width(),
                  height + .01, '%d%%'%int(difference[i]),
                  ha='center', va='bottom')
         i = i + 1

   percenterr(p1, p2)


#checks for arguments, given usage
if len(sys.argv) < 3:
   print "usage: " + sys.argv[0] + " [shempdata.csv pa1000data.csv]"
   exit(1)

shempread = open(sys.argv[1], 'r')
pa1000read = open(sys.argv[2], 'r')

#main regex loop
regex = re.compile('Vh[0-9]+m,-?[0-9]+\.?[0-9]*\s[A-Za-z_μ]+|'
                   'Ah[0-9]+m,-?[0-9]+\.?[0-9]*\s[A-Za-z_μ]+|'
                   'Wh[0-9]+m,-?[0-9]+\.?[0-9]*\s[A-Za-z_μ]+')
shempvoltage = []
shempamperage = []
shempwattage = []

for line in shempread:
   usefuldata = regex.findall(line)
   for word in usefuldata:
      #print word
      normalize_list(word, shempvoltage, shempamperage, shempwattage)

pavoltage = []
paamperage = []
pawattage = []

for line in pa1000read:
   usefuldata = regex.findall(line)
   for word in usefuldata:
      #print word
      normalize_list(word, pavoltage, paamperage, pawattage)
      
#usage, specify total number of plots, because I modified bar_graph to subplot
totalPlots = 1
#print wattage
plt.figure(num=1, figsize=(20,5))
#bar_graph(voltage, 'Voltage', 'r', totalPlots, 1)
bar_graph(shempamperage, paamperage, 'Amperage of 60W Lightbulb', 'rg', totalPlots, 1)
#bar_graph(wattage, 'Wattage', 'b', totalPlots, 3)

plt.show()

shempread.close()
pa1000read.close()

