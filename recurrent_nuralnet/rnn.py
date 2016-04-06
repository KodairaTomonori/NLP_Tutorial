import numpy
import pickle
import copy
import random
from collections import defaultdict


'''
    next: test

    
    Description: variable name  
    r: recurrent (meaningless)
    x: features
    y: labels
    o: output
    h: hidden
'''
numpy.random.seed(1)


def create_one_hot(index, size):
    vec = numpy.zeros(size)
    vec[index] = 1
    return vec


def create_map(fname):
    
    '''  file: word_pos word_pos .... '''
    x_ids = defaultdict(lambda: len(x_ids))
    y_ids = defaultdict(lambda: len(y_ids))
    word_label_list = list()
    x_y_list = list()
    for line in open(fname):
        x_list, y_list = list(), list()
        for one in line.strip().split(' '):
            x, y = one.split('_')
            x_list.append(x_ids[x])
            y_list.append(y_ids[y])
        x_y_list.append((x_list, y_list))
    x_size, y_size = len(x_ids), len(y_ids)
    
    for x_list, y_list in x_y_list:

        x_arrays, y_arrays = list(), list()
        for x, y in zip(x_list, y_list):
            x_arrays.append(create_one_hot(x, x_size))
            y_arrays.append(create_one_hot(y, y_size))
        word_label_list.append((numpy.array(x_arrays), numpy.array(y_arrays)))

    return x_ids, y_ids, word_label_list


    ''' probs: numpy.array '''
    return numpy.argmax(probs, 0)


def initialize(node_num, x_num, y_num):
    '''
        x_num: number of vocabluary
        y_num: number of pos
    '''
    random_array = lambda shape: numpy.random.rand(*shape) - .5
    hidden_layer = list()
    output_layer = list()
    # weight rx
    hidden_layer.append(random_array((node_num, x_num)))
    # weight rh
    hidden_layer.append(random_array((node_num, node_num)))
    # bias r
    hidden_layer.append(random_array((node_num,)))
    
    # weight_oh
    output_layer.append(random_array((y_num, node_num)))
    # bias o
    output_layer.append(random_array((y_num,)))

    return hidden_layer, output_layer 


def softmax(array):
    ex = numpy.exp(array)
    return ex / ex.sum()


def forward_rnn(weight_rx, weight_rh, bias_r, weight_oh, bias_o, x):
    '''
      hidden: values of hidden layer 
      probs: output probability
      y: index of max output probability
    '''
    x_length = len(x)
   
    hidden, probs, y = numpy.zeros((x_length, bias_r.shape[0])), numpy.zeros((x_length, bias_o.shape[0])), numpy.zeros(x_length)

    for time in range(x_length):
        if time > 0:
            hidden[time] = numpy.tanh(numpy.dot(weight_rx, x[time]) + numpy.dot(weight_rh, hidden[time - 1]) + bias_r)
        else:
            hidden[time] = (numpy.tanh(numpy.dot(weight_rx, x[time]) + bias_r))

        probs[time] = softmax(numpy.dot(weight_oh, hidden[time]) + bias_o)
        y[time] = numpy.argmax(probs[time], 0)
    return hidden, probs, y


def gradient_rnn(weight_rx, weight_rh, bias_r, weight_oh, bias_o, x, hidden, probs, y_, net_info):

    d_weight_rx, d_weight_rh, d_bias_r, d_weight_oh, d_bias_o = *net_info[0], *net_info[1]
    delta_r_ = numpy.zeros(len(bias_r))

    for time in range(len(x) - 1, -1, -1):
        delta_o_ = y_[time] - probs[time]
        d_weight_oh  += ((numpy.outer(hidden[time], delta_o_)).T)
        d_bias_o += delta_o_
        delta_r = numpy.dot(delta_r_, weight_rh) + numpy.dot(delta_o_, weight_oh)
        delta_r_ = delta_r * (1 - hidden[time]**2)
        d_weight_rx += numpy.outer(x[time], delta_r_).T
        d_bias_r += delta_r_

        if time != 0:
            d_weight_rh += numpy.outer(hidden[time-1], delta_r_)

    update_weights(weight_rx, weight_rh, bias_r, weight_oh, bias_o, 
        d_weight_rx, d_weight_rh, d_bias_r, d_weight_oh, d_bias_o, lam)



def update_weights(weight_rx, weight_rh, bias_r, weight_oh, bias_o, 
        d_weight_rx, d_weight_rh, d_bias_r, d_weight_oh, d_bias_o, lam):
    weight_rx += lam * d_weight_rx
    weight_rh += lam * d_weight_rh
    bias_r += lam * d_bias_r
    weight_oh += lam * d_weight_oh
    bias_o = lam * d_bias_o

def copy_layer(layer):
    return [x.copy() for x in layer]


def main():
    x_ids, y_ids, word_label_list = create_map(fname_word_label)
    f = open("ids.pkl", 'wb')
    pickle.dump([dict(x_ids), dict(y_ids)], f) 
    x_num, y_num = len(x_ids), len(y_ids)
    hidden_layer, output_layer = initialize(node_num, x_num, y_num)
    d_hidden_layer, d_output_layer = copy_layer(hidden_layer), copy_layer(output_layer)
    for _ in range(iteration):
        print(_) 
        accuracy = 0
        random.shuffle(word_label_list) 
        for features, labels in word_label_list[:300]:
            #print([numpy.argmax(y) for y in labels])
            hidden, probs, y_ = forward_rnn(*hidden_layer, *output_layer, features)
            #print(hidden, probs, y_)
            gradient_rnn(*hidden_layer, *output_layer, features, hidden, probs, 
                    labels, (copy_layer(d_hidden_layer), copy_layer(d_output_layer)))
            #update_weights(*hidden_layer, *output_layer, *delta_h, *delta_o, lam)
            #hidden, probs, y_ = forward_rnn(*hidden_layer, *output_layer, features)
            #print(hidden, probs, y_)
            accuracy += numpy.sum(numpy.argmax(labels) == y_)
        print(y_)   
        print(accuracy) 
            
    pickle.dump((hidden_layer, output_layer), open("layer.pkl", 'wb'))


if __name__ == "__main__":
    import sys
    iteration = 100   
    lam = 0.00001
    
    node_num = 64
    fname_word_label = "" if len(sys.argv) == 1 else sys.argv[1]

    main()
