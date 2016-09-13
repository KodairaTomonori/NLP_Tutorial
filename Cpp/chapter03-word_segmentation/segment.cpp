/*
 * unigram model file is made by chapter01.
 * usage: ./a.out model.txt test.txt
*/

#include <iostream>
#include <map>
#include <sstream>
#include <ostream>
#include <fstream>
#include <math.h>
#include <vector>


#include "../nlpmodules/process.hpp"

using namespace std;

#define LAMBDA 0.95
#define LAMBDA_UNK 0.05
#define VOCAB 100

const double UNK_PROB = LAMBDA_UNK / VOCAB;

struct Edge {
  Edge() : begin(), end() {}
  Edge(int x, int y) : begin(x), end(y) {}
  int begin, end;
};


typedef map<string, double> word_probability;
typedef map<int, double> score_map;
typedef map<int, Edge> edge_map;


word_probability load_model(char *fname) {
  word_probability wp;
  ifstream ifs(fname);
  string line;
  double prob;
  if (!ifs) {
    cout << fname << " is not found." << endl;
    exit (EXIT_FAILURE);
  } else {
    while (getline(ifs, line, '\n')) {
      stringstream ss_line(line);
      vector<string> words = stringSplit(line, '\t');
      sscanf(words[1].c_str(), "%lf", &prob);
      wp[words[0]] = prob;
    }
  }
  return wp;
}


edge_map forward(string sentence, word_probability &wp) {
  score_map best_score;
  edge_map best_edge;
  best_edge[0] =  Edge(-1, 0);
  best_score[0] = 0.0;

  for (int end = 3; end <= sentence.length(); end += 3) {
    best_score[end] = 10000000000;
    for (int begin = 0; begin < end; begin += 3) {
      int word_len = (end - begin) ;
      int begin_index = begin ;
      string sub = sentence.substr(begin_index, word_len);
      if (wp.find(sub) != wp.end() || word_len == 3) {
        double prob = wp.find(sub) != wp.end() ? wp[sub] * LAMBDA : UNK_PROB;
        double sub_score = best_score[begin] - log(prob);
        if (sub_score < best_score[end]) {
          best_score[end] = sub_score;
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
    word = sentence.substr(next_edge.begin, (next_edge.end - next_edge.begin));
    words.insert(words.begin(), word);
    next_edge = best_edge[next_edge.begin];
  }
  return words;
}



void segment(char *model_f, char *test_f) {
  char output_f[] = "./data/result.txt";
  ifstream ifs(test_f);
  ofstream ofs(output_f);
  string sentence;
  if (!ifs) {
    cout << test_f << " is not found." << endl;
    exit (EXIT_FAILURE);
  }
  // load unigram probability
  cout << "load model file" << endl;
  word_probability wp = load_model(model_f);
  cout << "start segment" << endl;
  while (getline(ifs, sentence, '\n')) {
    edge_map best_edge = forward(sentence, wp);
    vector<string> words = back_step(sentence, best_edge);
    for (vector<string>::iterator it = words.begin(); it != words.end(); it ++)
      ofs << *it << " ";
    ofs << '\n';
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

