#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <functional>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;


typedef unordered_map<string, int> Counter;


void add(vector<string> ngram_words, Counter &temp_map, int n) {
  string concat_word = ngram_words[0];
  for (int i = 1; i < n-1; i ++) {
    concat_word += " " + ngram_words[i];
  }
  temp_map[concat_word] += 1;
  if (n != 1) {
    concat_word += " " + ngram_words[n-1];
    temp_map[concat_word] += 1;
  } 
}


void count_ngram(char *fname, int N, Counter &counter) {
  ifstream ifs(fname);
  string sentence, word;
  vector<string> words;
  bool flag = false;

  if (!ifs) {
    cout << fname << " is not found." << endl;
    return;
  } else {
    while (getline(ifs, sentence, '\n')) {
      flag = false;
      stringstream ss_sentence("<s> " + sentence + " </s>");
      while (getline(ss_sentence, word, ' ')) {
        counter[""] += 1;
        words.push_back(word);
        if (!flag && words.size() == N) {
          flag = true;
        }
        if (flag) {
          add(words, counter, N);
          words.erase(words.begin());
        }
      }
      words.clear();
    }
  }
  return;
}


string get_context(string words) {
  size_t last_index = words.rfind(" ");
  if (last_index != string::npos) return words.substr(0, last_index);
  else return "";
}


void print_content(Counter temp, char *fout) {
  ofstream os_fout(fout);
  for (auto i = temp.begin(); i != temp.end(); i++) {
    //int a = temp[get_context(i->first)];
    //if (a == 0) cout << i->first << endl;
    os_fout << i->first << "\t" << (float)i->second / temp[get_context(i->first)] << endl;
  }
}


int main (int argc, char* argv[]) {
  Counter Ngram_counter;
  char *fname = (char *)"../data/wiki-en-train.word";
  char *fout = (char *)"model.tsv";
  int N = 2;

  for (int i = 0; i < argc; i++) {
    string a(argv[i]);
    if (a == "-n") N = atoi(argv[i+1]);
    else if (a == "-f") fname = argv[i+1];
    else if (a == "-o") fout = argv[i+1];
  }

  cout << "make " << N << "-gram model." << endl;
  cout << "input file: " << fname << endl;
  cout << "output file: " << fout << endl;

  count_ngram((char *)fname, N, Ngram_counter);
  print_content(Ngram_counter, fout);

  return 0;
}
