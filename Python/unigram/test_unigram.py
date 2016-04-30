#!/usr/bin/python
#coding: UTF-8
import sys
import math

#-------------load file-------------
model_file = open(sys.argv[1], "r")
test_file = open(sys.argv[2], "r")


#----------- Initial value --------
lam1 = 0.95
lam_unk = 0.05
V = 1000000
W = 0
H = 0.0
unk = 0

# create map probabilities
probabilities = {}

# ----------- load model ------------

# for each line in model_file
for line in model_file:
    
    # split line into w and P
    sentence = line.strip()
    words = sentence.split(" , ")
    
    # set probabilities[w] = P
    probabilities[words[0] ] = float(words[1])



#--------------evaluate -------------
# for each line in test_file
for line in test_file:
  # split line into an array of words
  sentence = line.strip()
  words = sentence.split(' ')
  # append "</s>" to the end of words
  words.append('</s>')
  # for each w in words
  for w in words:
    
    # add 1 to W
    W += 1
    
    # set P += λ_unk  / V
    P = lam_unk / V
    
    # if probabilities[w] exists
    if w in probabilities:
        
      # set P += λ1 * probabilities[w]
      P += lam1 * probabilities[w]
    else:
      # add 1 to unk
      unk += 1
    
    # add -log2 P to H
    H += -1 * math.log(P, 2)

#------------result-----------------
print 'words = ' + str(W)
print 'entropy = ' +  str(H / W)
print 'coverage = ' + str((W - unk) / float(W) )

