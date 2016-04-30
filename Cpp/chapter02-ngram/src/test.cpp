#include<sstream>
#include<fstream>
#include<iostream>
#include<unordered_map>
#include<cstdlib>
#include<vector>
using namespace std;

typedef unordered_map<string, float> ProbMap;

const float _lam = 0.95;
float V = 1000000;

void load_prob(char *fname, ProbMap &prob_map) {
  ifstream ifs(fname);
  bool flag;
  string ngram, line, word;
  int c = 0;
  if (!ifs) {
    cout << fname << " is not found." << endl;
  } else {
    while (getline(ifs, line, '\n')) {
      stringstream ss_line(line);
      flag = true;
      while (getline(ss_line, word, '\t')) {
        if (flag) {
          ngram = word;
          flag = false;
        } else {
          prob_map[ngram] = atof(word.c_str());
        }
      }
    }
  }    
  return;
}

float log_prob(ProbMap &prob_map, vector<string> &words, vector<float> &lambdas) {
  float p = 0.0; 
  int N = words.size();
  string concat_word;
  bool flag = true;
  int j = 0;
  for (auto i = words.rbegin(); i != words.rend(); i ++, j ++) {
     if (flag) {
       concat_word = *i; 
       p = lambdas[j] * prob_map[concat_word] + (1 - lambdas[j]) / V;
       flag = false;
     } else {
       concat_word = *i + " " + concat_word; 
       p = lambdas[j] * prob_map[concat_word] + (1 - lambdas[j]) * p;
     }
  }
  return -log2(p);
}


void test_ngram(int n, char *fname, vector<float> &lambdas, ProbMap &prob_map) {
  ifstream ifs(fname);
  string line, word;
  vector<string> words;
  bool flag;
  float H;
  int word_count = 0;

  if (!ifs) {
    cout << fname << " is not found." << endl;
  } else {
    while (getline(ifs, line, '\n')) {
      line = "<s> " + line + " </s>";
      stringstream ss_line(line);
      flag = false;
      while (getline(ss_line, word, ' ')) {
        words.push_back(word);
        if (!flag && words.size() == n) {
          flag = true;
        }
        if (flag) {
          H += log_prob(prob_map, words, lambdas);
          words.erase(words.begin());
          word_count += 1;
        }
      }
      words.clear();
    }
  }
  cout << H / word_count << endl;
}


int main(int argc, char *argv[]) {
  ProbMap prob_map;
  char *prob_file = (char*)"../data/model.tsv";
  char *fname = (char*)"../data/wiki-en-test.word";
  int N = 2;
  vector<float> lambdas(N, _lam);
  
  for (int i = 0; i < argc; i++) {
    string a(argv[i]);
    if (a == "-n") N = atoi(argv[i+1]);
    else if (a == "-f") fname = argv[i+1];
    else if (a == "-m") prob_file = argv[i+1];
  }

  cout << "model file (-m) is " << prob_file << endl;
  cout << "test file (-f) is " << fname << endl;
  cout << N << "-gram (-n) model" << endl;

  load_prob(prob_file, prob_map);
  test_ngram((int)N, fname, lambdas, prob_map); 
  
  return 0;
}

