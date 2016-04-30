#include <iostream>
#include <unordered_map>
#include <sstream>
#include <fstream>
#include <math.h>


using namespace std;


// global variables
const float lam_1 = 0.95;
const float lam_unk = 1 - lam_1;
const int V = 1000000;
unordered_map<string, float> model;


// load unigram model file
int load_model(char *fname) {
  string line, word, one;
  ifstream ifs(fname);
  bool flag = true;
  float prob;

  if (!ifs) {
    cout << fname << " is not found." << endl;
    return -1;
  } else {
    while (getline(ifs, line, '\n')) {
      stringstream ss_line(line);
      while (getline(ss_line, one, '\t')) {
        if (flag) {
          flag = false;
          word = one;
        } else {
          flag = true;
          sscanf(one.c_str(), "%f", &prob);
          model[word] = prob;  
        }
      }
    }
  }
  return 0;
}


// culc entropy and coverage
int test(char *fname) {
  string line, word;
  ifstream ifs(fname);
  // W: word count
  float W, H, P;
  int unk = 0;
  if (!ifs) {
    cout << fname << " is not found." << endl;
    return -1;
  }
  while (getline(ifs, line, '\n')) {
    line += " </s>";
    stringstream ss_line(line);
    while (getline(ss_line, word, ' ')) {
      W += 1;
      P = lam_unk / V;
      if (model.find(word) != model.end())
        P += lam_1 * model[word];
      else 
        unk ++;
      H -= log2(P);
    }
  }
  cout << unk << endl;
  cout << "entropy = " << H / W << endl;
  cout << "coverage = " << (W - unk) / float(W) << endl;
  return 0;
}


// write file to argv[2]
void print(char *fname) {
  //ofstream ofs(fname); 
  for (auto it = model.begin(); it != model.end(); it ++)
     cout << it->first << '\t' << float(it->second) << endl;
}


int main(int argc, char *argv[]){
  string one;
  if (load_model(argv[1]) < 0) return -1;
  print(argv[1]);
  test(argv[2]);
  return 0;
}

