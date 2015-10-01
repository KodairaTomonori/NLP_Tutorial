#!/usr/bin/python
# python train_hmm.py
from collections import defaultdict

# train hidden markov model
# input data format is "natural_JJ language_NN ..."

def hmm_train(f_name, output_file_name):
    # 
    emit = defaultdict(lambda: 0)
    transition = defaultdict(lambda: 0)
    context = defaultdict(lambda: 0)

    for line in open(f_name):
        # set beginning symbol "<s>"
        previous = "<s>"
        # count "<s>"
        context[previous] += 1
        wordtags = line.strip().split(" ")

        for wordtag in wordtags:
            word, tag = wordtag.split("_")
            if previous is not "":
                # count transition
                transition[previous + " " + tag] += 1
            # count context
            context[tag] += 1
            #count emit
            emit[tag + " " + word] += 1
            previous = tag
        # count transition to </s>
        transition[previous + " </s>"] += 1

    # write output file
    write_dict_file(output_file_name, transition, emit, context)



def write_dict_file(fout_name, transition, emit, context):
    fout = open(fout_name, "w")

    for key, value in sorted(transition.items() ):
        previous, word = key.split(" ")
        line = "T " +  key + " " +  str(float(value) / context[previous]) + "\n"
        fout.write(line)
    
    for key, value in sorted(emit.items() ):
        tag, word = key.split(" ")
        line = "E " +  key + " " +  str(float(value) / context[previous]) + "\n"
        fout.write(line)

    fout.close()

if __name__ == "__main__":
    file_name = 'train.txt'
    output_file_name = 'train_hmm.txt'
    hmm_train(file_name, output_file_name)
    
    
