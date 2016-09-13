#include <iostream>
#include <map>
#include <sstream>
#include <fstream>
#include <math.h>
#include <vector>

#include "../nlpmodules/process.hpp"

using namespace std;

#define LAMBDA 0.95
#define LAMBDA_UNK 0.05
#define VOCAB 1000000

const float UNK_PROB = LAMBDA_UNK / VOCAB;

struct Edge {
  Edge() : begin(), end() {}
  Edge(int x, int y) : begin(x), end(y) {}
  int begin, end;
};


typedef map<string, float> word_probability;
typedef map<int, float> score_map;
typedef map<int, Edge> edge_map;


word_probability load_model(char *fname) {
  word_probability wp;
  ifstream ifs(fname);
  string line;
  float prob;
  if (!ifs) {
    cout << fname << " is not found." << endl;
    exit (EXIT_FAILURE);
  } else {
    while (getline(ifs, line, '\n')) {
      stringstream ss_line(line);
      vector<string> words = stringSplit(line, '\t');
      sscanf(words[1].c_str(), "%f", &prob);
      wp[words[0]] = prob;
    }
  }
  cout << endl;
  return wp;
}


edge_map forward(string sentence, word_probability &wp) {
  score_map best_score;
  edge_map best_edge;
  best_edge[0] =  Edge(-1, 0);
  best_score[0] = 0.0;
  for (int end = 1; end <= sentence.length(); end ++) {
    best_score[end] = 10000;
    for (int begin = 0; begin != end; begin ++) {
      int word_len = end - begin;
      string sub = sentence.substr(begin, word_len);
      if (wp.find(sub) != wp.end() || word_len == 1) {
        float prob = wp.find(sub) != wp.end() ? wp[sub] * LAMBDA : UNK_PROB;
        float sub_score = best_score[begin] - log(prob);
        if (sub_score < best_score[end]) {
          best_score[end] = sub_score;
          cout << end <<  sub << " " << best_score[end] << endl;
          best_edge[end] = Edge(begin, end);
        }
      }
    }
  }
  return best_edge;
}


vector<string> back_step(string sentence, edge_map best_edge) {
  Edge next_edge = best_edge[sentence.length()];
  vector<string> words;
  string word;
  while (next_edge.begin != -1) {
    word = sentence.substr(next_edge.begin, next_edge.end - next_edge.begin);
    cout << next_edge.begin << " " << next_edge.end << " " << word << endl;
    words.insert(words.begin(), word);
    next_edge = best_edge[next_edge.begin];
  }
  return words;
}



void segment(char *model_f, char *test_f) {
  ifstream ifs(test_f);
  string sentence;
  word_probability wp = load_model(model_f);
  if (!ifs) {
    cout << test_f << " is not found." << endl;
    exit (EXIT_FAILURE);
  }
  cout << "start segment" << test_f << endl;
  while (getline(ifs, sentence, '\n')) {
    edge_map best_edge = forward(sentence, wp);
    vector<string> words = back_step(sentence, best_edge);
    for (vector<string>::iterator it = words.begin(); it != words.end(); it ++)
      cout << *it << " ";
    cout << endl;
  }
}


int main(int argc, char *argv[]) {
  if (argc < 3) {
    cout << "Please input:" << endl;
    cout << "\t1: model file\n\t2: test file" << endl;
    return -1;
  } else {
    cout << "model file is " << argv[1] << endl << "test file is " << argv[2] << endl;
  }
  segment(argv[1], argv[2]);
}

