#coding: utf-8
# 2-gramモデルを学習


if __name__ == "__main__":
  
  from collections import defaultdict
  
  counts = defaultdict(lambda: 0)
  context_counts = defaultdict(lambda: 0)
  
  import sys
  training_file = open(sys.argv[1], 'r')


  for line in training_file:
      
    line = line.strip()
    words = line.split(' ')
    words.append('</s>')
    words.insert(0, '<s>')

    for i in range(1, len(words) - 1):
                   
      bigram = ' '.join(words[i - 1:i + 1])
      
      counts[bigram] += 1
      
      context_counts[words[i - 1] ] += 1
      
      counts[words[i] ] += 1
                        
      context_counts[''] += 1
   
                        
  model_file = open(sys.argv[2], 'w')
  
  for ngram, count in counts.items():
                        
    words = ngram.split(' ')
    words.pop()
    context = ''.join(words)
    
    probability = 1
    if context_counts[context] == 0:
      print context
    probability = float(counts[ngram]) / context_counts[context]
    model_file.write(ngram + '\t' + str(probability) + '\n')
