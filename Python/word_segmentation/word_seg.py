#coding:utf-8

# import module
import sys
import math
from collections import defaultdict


# Read the  file to dictionary separated by ' , '
def LoadDictFile(file): 
  file_dict = defaultdict(lambda : 0)

  for line in file:
    line_list = line.strip().split(' , ')
    file_dict[unicode(line_list[0], 'utf-8') ] = float(line_list[1])
  return file_dict 


# culcurate probability
def culUniProb(w, probabilities):
  lam1 = 0.95
  lam_unk = 0.05
  V = 1000000

  P = lam_unk / V
  if w in probabilities:
    P += lam1 * float(probabilities[w])
  return P


 # maemuki suteppu
def forward_step(line, uni_prob, best_edge):
  best_score = {0 : 0}
  for word_end in range(1, len(line) + 1):
    best_score[word_end] = math.pow(10, 10)

    for word_begin in range(0, word_end ):
      word = line[word_begin : word_end]
      if word in uni_prob or len(word) == 1:
        prob = culUniProb(word, uni_prob)
        my_score = best_score[word_begin] - math.log(prob)
        
        if my_score < best_score[word_end]:
          best_score[word_end] = my_score
          best_edge[word_end] = (word_begin, word_end)
    # end fo rward_step


# usiromukisuteppu
def back_step(best_edge, line):
  words = []
  next_edge = best_edge[len(best_edge) - 1] 
  while next_edge != 'NULL':
    word = line[next_edge[0] : next_edge[1] ]
    word = word.encode('utf-8')
    words.append(word)
    next_edge = best_edge[next_edge[0] ]

  words.reverse()
  return ' '.join(words)
  
  
# bitabbi
def word_seg(uni_file, input_file):
  
  uni_prob = LoadDictFile(uni_file)
  for line in input_file:     
    best_edge = {0 : 'NULL'}
    line = unicode(line.strip(), 'utf-8')
    forward_step(line, uni_prob, best_edge)
    print back_step(best_edge, line) 



if __name__ == '__main__':
  unigram = open(sys.argv[1], 'r')
  input_file = open(sys.argv[2], 'r')
  word_seg(unigram, input_file)  
  
