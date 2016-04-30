#!usr/bin/python
# python test_hmm.py train_hmm.txt test.txt
# evaluation: perl ../../script/gradepos.pl ../../data/wiki-en-test.pos ans.txt
import sys
import math
from collections import defaultdict

# load model file
def load_model(f_name):
    transition = {}
    emission = defaultdict(lambda: 0.00000005)
    possible_tags = {}

    for line in open(f_name):
        types, context, word, prob = line.strip().split(" ")
        possible_tags[context] = 1
        if types == "T":
            # context = previous_pos  , word = next_pos
            transition[context + " " + word] = float(prob)
        else:
            # context = pos
            emission[context + " " + word] = float(prob)
    
    return transition, emission, possible_tags


# forward step
def forward_step(words, transition, emission, possible_tags):
    l = len(words)
    best_score = {"0 <s>": 0}
    best_edge = {"0 <s>": "NULL"}
    for i in range(0, l):
        for prev in possible_tags.keys():
            for nexts in possible_tags.keys():
                prev_next = prev + " " + nexts
                i_prev = str(i) + " " + prev
                if i_prev in best_score and prev_next in transition:
                    i1_next = str(i + 1) + " " + nexts
                    next_word = nexts + " " + words[i]
                    # score = best_score[prev] - log Pt(prev_pos | next_[pos)
                    #                          - log Pe(word | nexts_os)
                    score = float(best_score[i_prev]) \
                            - math.log(float(transition[prev_next] * 0.95) ) \
                            - math.log(float(emission[next_word ] * 0.95) )
                    # update best_score and best_edge
                    if i1_next not in best_score \
                            or best_score[i1_next] > score:
                        best_score[i1_next] = score
                        best_edge[i1_next] = i_prev
        
    # culclate score and edge when word = </s>
    for prev in possible_tags.keys():
        len_prev = str(l) + " " + prev
        prev_s = prev +  " </s>"
        if len_prev in best_score and prev_s in transition:
            score = best_score[len_prev] \
                    - math.log(transition[prev_s])
            i1_s = str(len(words) + 1) + " </s>"
            if i1_s not in best_score or best_score[i1_s] > score:
                best_score[i1_s] = score
                best_edge[i1_s] = len_prev
                    
    return best_edge


# back step
def back_step(best_edge, words):
    tags = []

    next_edge = best_edge[str(len(words) + 1 ) + " </s>"]
    
    while next_edge != "0 <s>":
        position, tag = next_edge.split(" ")
        tags.append(tag)
        next_edge = best_edge[next_edge]
    tags.reverse()
    return  " ".join(tags)


# hidden marcov model  , estimate pos
def hmm(m_filename, t_filename):
    transition, emission, possible_tags = load_model(m_filename)

    for line in open(t_filename):
        words = line.strip().split(" ")
        best_edge = forward_step(words, transition, emission, possible_tags)
        tags_word = back_step(best_edge, words)
        print tags_word



if __name__ == "__main__":
    
    hmm(sys.argv[1], sys.argv[2])
