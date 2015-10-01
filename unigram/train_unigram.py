#!/usr/bin/python
# coding: UTF-8
from collections import defaultdict
import sys

#load file
my_file = open(sys.argv[1], "r")

#初期値の設定
my_dict = defaultdict(lambda: 1)
num = 0

for line in my_file:
  # 行ごとに分ける
  sentence = line.strip()
  #空白で区切る
  words = sentence.split(" ")
  words.append('</s>')
  #単語ごとにカウント
  for word in words:
    num += 1
    if word in my_dict:
      my_dict[word] += 1
    else:
      my_dict[word]
for word in my_dict:
  my_dict[word] /= float(num)

model_file = open('model_file.txt', 'w')


for foo, bar in  sorted(my_dict.items() ):
   model_file.write("%s , %r\n" % (foo, bar) )
model_file.close()