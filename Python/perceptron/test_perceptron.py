#coding: utf-8

from train_perceptron import *
from collections import defaultdict
import sys


# predict all case
def predictAll(model_file, input_file, output_file):
  w = defaultdict(lambda : 0)
  
  # load weight from modelfile
  for line in model_file:
    line = line.strip().split('\t')
    w[line[0] ] = int(line[1])

  # predict   
  for x in input_file:
    phi = createFeatures(x)
    y_ = predictOne(w, phi)
    output_file.write(str(y_) + '\n')
#end def predictAll

if __name__ == '__main__':
  model_file = open(sys.argv[1], 'r')
  input_file = open(sys.argv[2], 'r')
  ans_file = open(sys.argv[3], 'w')
  predictAll(model_file, input_file,  ans_file)
