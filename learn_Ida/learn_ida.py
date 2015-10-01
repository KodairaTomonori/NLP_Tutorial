#!usr/bin/python

import random

from collections import defaultdict
import sys
import math


def sample_one(probs):
    z = sum(probs)
    remaining = random.uniform(0, z)
    for i in range(0, len(probs) ):
        remaining -= probs[i]
        if remaining <= 0:
            return i
            
    print 'error'
    exit()

def add_count(word, topic, doc_id, amount):
    xcounts[str(topic)] += amount
    xcounts[word + ' ' + str(topic)] += amount
    
    ycounts[str(doc_id)] += amount
    ycounts[str(topic) + ' ' + str(doc_id)] += amount


def initialize(file_name):
    for line in open(file_name):
        doc_id = len(xcorpus)
        topics = list()
        words = line.strip().split()
        for word in words:
            topic = random.randint(0, num_topics - 1) 
            topics.append(topic)
            add_count(word, topic, doc_id, 1)
        xcorpus.append(words)
        ycorpus.append(topics)


def topic_prob(topic, word, doc_id):
    prob = ((xcounts[word + ' ' + str(topic)] + alp) \
        / (xcounts[str(topic)] + alp * 8) )\
        * ((ycounts[str(topic) + ' ' + str(doc_id)] + beta) \
        / (ycounts[str(doc_id)] + beta * num_topics ) )
        
    #print (xcounts[word + ' ' + str(topic)] + alp) / (xcounts[str(topic)] + alp *  8),(ycounts[str(topic) + ' ' + str(doc_id)] + beta) / (ycounts[str(doc_id)] + beta * num_topics )  
        
    return prob


def sampling(ll):
    for i in range(0, len(xcorpus) ):
        for j in range(0, len(xcorpus[i]) ):
            x = xcorpus[i][j]
            y = ycorpus[i][j]
            add_count(x, y, i, -1)
            probs = list()
            for k in range(0, num_topics):
                probs.append(topic_prob(k, x, i) )
            new_y = sample_one(probs)
            ll -= math.log(probs[new_y])
            add_count(x, new_y, i, 1)
            ycorpus[i][j] = new_y
        print ll
    return ll

def print_result():
    result=defaultdict(list)
    for doc_id in range(0, len(xcorpus)):
        for word_id in range(0, len(xcorpus[doc_id])):
            result[ycorpus[doc_id][word_id]].append(xcorpus[doc_id][word_id])
        
    for topic, words in result.items():
        print topic, ": ",
        for word in sorted(set(words)):
            print word,
        print ""


def learn_ida(file_name):
    initialize(file_name)
    ll = 0
    for num in range(roop_num):
        ll = sampling(ll)
        
    print_result()

if __name__ == '__main__':
    xcorpus = list(); ycorpus = list()
    xcounts = defaultdict(int); ycounts = defaultdict(int)
    alp = 0.001; beta = 0.001
    file_name = sys.argv[1]
    roop_num = 1000
    num_topics = 30
    
    learn_ida(file_name)
