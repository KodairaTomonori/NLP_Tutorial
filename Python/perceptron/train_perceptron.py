#coding: utf-8

# import module
from collections import defaultdict
import sys

# prediction for one case
def predictOne(w, phi):
  score = 0
  
  # culcurate score
  for name, value in phi.items():
    if name in w:
      score += value * w[name]
    print name, value
     
  # output yes or no
  if score >= 0:
    return 1
  else:
    return - 1


# create features of uni-gram(x = one sentence)
def createFeatures(x):
  phi = defaultdict(lambda : 0)
  words = x.split(' ')
  
  # count number of occurrence(uni-gram)
  for word in words:
    phi['UNI:' + word] += 1

  return phi


# update weights by perceptron
def updateWeights(w, phi, y):
  for name, value in phi.items():
    w[name] += int(value) * int(y)


# online learning
def onlineLearning(train_file):
  w = defaultdict(lambda : 0)
  for sentence in train_file:
    y, x = sentence.strip().split('\t')
    phi = createFeatures(x)
    y_ = predictOne(w, phi)
    if y_ != y:
      updateWeights(w, phi, y)
  return w


# write file 
def writeDictToFile(fin, fout):
  for i, j in fin.items():
    fout.write(str(j) + '\t' + i + '\n' ) 


if __name__ == '__main__':
  train_file = open(sys.argv[1], 'r')
  model_file = open(sys.argv[2], 'w')
  writeDictToFile(onlineLearning(train_file), model_file)

  model_file.close()



