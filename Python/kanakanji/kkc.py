#!usr/bin/python
# python test_hmm.py train_hmm.txt test.txt
# evaluation: perl ../../script/gradepos.pl ../../data/wiki-en-test.pos ans.txt
import sys
import math
from collections import defaultdict

# load model file
def load_tm(f_name):
    tm = defaultdict(dict) 
    
    for line in open(f_name):
        types, context, word, prob = line.strip().split(" ")
        tm[context][word] = float(prob)
    
    return tm


def load_lm(f_name):
    probs = defaultdict(lambda: 0.00000005)
    for line in open(f_name):
        line = line.strip()
        words = line.split('\t')
        probs[words[0] ] = float(words[1])


# forward step
def forward_step(words, tm, lm):
    best_score = {0: {'<s>': 0} }
    best_edge = {0: {"<s>": "NULL"} }
    for end in range(1, len(words) ):
        best_score[end] = {}
        best_edge[end] = {}
        for begin in range(end):
            pron = words[begin : end]
            my_tm = tm[pron]
            if len(my_tm) == 0  or len(pron) == 1:
                my_tm = (pron, 0)
            print my_tm
            for curr_word, tm_prob in my_tm:
                for prev_word, prev_score in score[begin]:
                    curr_score = prev_score - math.log(tm_prob * \
                        lm[prev_word + " " + curr_word] )
                    if curr_score < best_score[end][curr_word]:
                        best_score[end][curr_word] = curr_score
                        best_edge[end][curr_word] = (begin, prev_word)
    return best_edge


# back step
def back_step(best_edge, words):
    tags = []
    next_edge = best_edge[len(words)][ "</s>"]    
    while next_edge != "0 <s>":
        position, tag = next_edge.split(" ")
        tags.append(tag)
        next_edge = best_edge[next_edge]
    tags.reverse()
    return  " ".join(tags)


# hidden marcov model  , estimate pos
def hmm(lm_fname, tm_fname, out_fname):
    tm = load_tm(tm_fname)
    lm = load_lm(lm_fname)
    for line in open(out_fname):
        words = line.strip().decode('utf-8')
        best_edge = forward_step(words, tm, lm)
        tags_word = back_step(best_edge, words)
        print tags_word



if __name__ == "__main__":
    
    hmm(sys.argv[1], sys.argv[2], sys.argv[3])
