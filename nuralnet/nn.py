#!usr/bin/python
#coding:utf8
from collections import defaultdict
from collections import Counter
import numpy as np
test_flag = True
train_flag = True

def forward_nn(network, phi_zero):
    phi = [phi_zero]
    for i in range(0, len(network)):
        w, b = network[i]
        phi.append(np.tanh(np.dot(w, phi[i]) + b ) )
    return phi


def backward_nn(net, phi, y_):
    J = len(net)
    delta_ = [[]] * (J + 1)
    delta = list(delta_);
    delta[J] = np.array(y_ - phi[J][0])
    for i in range(J - 1, -1, -1):
        delta_[i + 1] = np.array(delta[i + 1] * (1 - phi[i + 1] * phi[i + 1]) )
        w, b = net[i]
        delta[i] = (np.dot(delta_[i + 1], w) )
    return delta_


def update_weights(net, phi, delta_, rambda):
    for i in range(len(net) ):
        net[i][0] += rambda * np.outer(delta_[i + 1], phi[i])
        net[i][1] += rambda * delta_[i + 1]

def create_features(x, phi, test=False):
    words = x.strip().split()
    for word in words:
        if test and 'UNI' + word not in ids: continue
        phi[ids['UNI' + word] ] += 1
    return phi


def count_features(train_file):
    return len(set(train_file.read() \
        .replace('\n', ' ').replace('\t', ' ').split(' ') ) ) - 2


# bias_nums: 次の層のノードの数（最初は素性の数）
def init_net(feature_num, bias_nums=[2, 1]):
    net = list()
    layer_node_num = [feature_num] + [i for i in (bias_nums[:-1])]
    # それぞれのノードの数の分の重みとバイアスのペアを、次のノードの分だけ生成
    for next_num, node_num in enumerate(layer_node_num):
        weights = list(); biases = list()
        for i in range(bias_nums[next_num]):
            weights.append(np.random.rand(node_num) - 0.5)
            biases.append((np.random.rand(1) - 0.5)[0])
        net.append([weights, biases])
    return net


def initialize(train_file):
    feat_lab = list()
    zeros = np.zeros(count_features(train_file) )
    train_file.seek(0)
    for line in train_file:
        y, x = line.strip().split('\t')
        feat_lab.append((create_features(x, zeros.copy() ), int(y) ) )
    return feat_lab, init_net(len(zeros) )


def nural_net(train_file, ite):
    feat_lab, net = initialize(train_file)
    rambda = 0.1
    pre_error_count = 1000000000000000000
    for i in range(ite):
        error_count = 0
        for phi_zero, y in feat_lab:
            phi = forward_nn(net, phi_zero)
            if (y > 0 and phi[-1][-1] < 0) or \
                (y < 0 and phi[-1][-1] > 0): error_count += 1 
            delta_ = backward_nn(net, phi, y)
            update_weights(net, phi, delta_, rambda)
        if error_count > pre_error_count: rambda *= 0.9
        pre_error_count = error_count
        print error_count
    return net


def test(model, test_file):
    feat_zeros = np.zeros(len(ids) )
    fout = open('output.txt', 'w')
    for line in open(test_file):
        phi_zero = create_features(line, feat_zeros.copy(), True)
        phi = forward_nn(model, phi_zero)
        fout.write(str(phi[-1][-1]) + '\n')
    print 'finish_test'
            

        
if __name__ == '__main__':
    ite = 10
    import pickle
    ids = defaultdict(lambda: len(ids) )
    if train_flag:
        model = nural_net(open('input.txt'), ite)
        pickle.dump([model, dict(ids)], open('model.pkl', 'w') )
    else: model, ids = pickle.load(open('model.pkl') )
    if test_flag:
        test(model, 'test.txt')
