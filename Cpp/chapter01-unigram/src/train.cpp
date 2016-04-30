#include <iostream>
#include <unordered_map>
#include <sstream>
#include <fstream>
#include <math.h>


using namespace std;


// global variables
unordered_map<string, float> word_counter;
int total_word_count = 0; 

// count unigram
int train_unigram(char *fname) {
  string line, word;
  ifstream ifs(fname);

  if (!ifs) {
    cout << fname << " is not found." << endl;
    return -1;
  } else {
    while (getline(ifs, line, '\n')) {
      line += " </s>";
      stringstream ss_line(line);
      while (getline(ss_line, word, ' ')) {
        total_word_count += 1;
        word_counter[word] += 1;
      }
    }
  }
  
  return 0;

}


// write file to argv[2]
void print(char *fname) {
  ofstream ofs(fname); 
  for (auto it = word_counter.begin(); it != word_counter.end(); it ++)
     ofs << it->first << '\t' << float(it->second) / total_word_count << endl;
}


int main(int argc, char *argv[]){
  string one;

  if (argc < 2) {
    cout << argc << endl;
    cout << "Pleasse input:" << endl;
    cout << "1: input file name" << endl;
    cout << "2: output file name for model" << endl;
    return -1;
  }
  train_unigram(argv[1]);
  print(argv[2]);
  return 0;
}

