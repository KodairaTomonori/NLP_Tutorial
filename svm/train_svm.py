#!usr/bin/python

from collections import defaultdict
import math


def create_features(x):
    phi = defaultdict(int)
    for word in x.strip().split():
        phi['UNI:' + word] += 1
    return phi


def sign(value):
    if value / abs(value) >= 0:
        return 1
    else:
        return -1

def getw(w, name, c, ite, last):
    if ite != last[name]:
        c_size = c * (ite - last[name])
        if abs(w[name]) <= c_size:
            w[name] = 0
        else:
            w[name] -= sign(w[name]) * c_size
        last[name] = ite
    return w[name]
        
 

def update_weight(w, phi, y, c):
    for name, value in w.items():
        if abs(value) < c:
            w[name] = 0
        else:
            w[name] -= sign(value) * c
    for name, value in phi.items():
        w[name] += value * y


def online_train(train_file, c, margin, w, last, ite):

    for line in train_file:
        y, x = line.strip().split('\t')
        y = int(y)
        phi = create_features(x)
        val = sum(getw(w, name, c, ite, last) * phi[name] * y for name in phi.keys() )
        #if val <= margin:
        #    update_weight(w, phi, y, c)


def predict(file_name, w):
    for line in open(file_name):
        score = 0
        phi = create_features(line)
        for word in line.strip().split():
            score += phi['UNI:' + word] * w['UNI:' + word]
        if score >= 0:
            print 1
        else:
            print -1

def itelation(num, function):
    for i in range(1, num + 1):
        function(train_file, c, margin, w, last, i)
        train_file.seek(0)
 
if __name__ == '__main__':
    train_file = open('train.labeled', 'r')
    test_file = 'test.word'
    last = defaultdict(int)
    margin = .1
    c = .0001
    w = defaultdict(float)
    num = 100 
    itelation(num, online_train) 
    predict(test_file, w)


