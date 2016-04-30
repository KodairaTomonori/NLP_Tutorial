#include <iostream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <functional>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;


struct hashing_func {
    unsigned long operator()(const string& key) const {
        unsigned long hash = 0;
        int seed = 131;
        const char* str = key.c_str();
        //for(size_t i=0; i<key.size(); i++)
        while (*str) {
          hash +=  (hash * seed) + *str;
          str ++;
        } 
        return hash & (0x7FFFFFFF);
    }
};


struct key_equal_fn {
    bool operator()(const string& t1, const string& t2) const {
        return !(t1.compare(t2));
    }
};


struct my_equal_to {
  bool operator()(const char *__x, const char *__y) const {
    return strcmp(__x, __y) == 0;
  }
};

typedef unordered_map<string, int, hashing_func, key_equal_fn> MapType;



void add(vector<string> ngram_words, MapType &temp_map, int n) {
  string concat_word = ngram_words[0];
  for (int i = 1; i < n-1; i ++) {
    concat_word += " " + ngram_words[i];
  }
  temp_map[concat_word] += 1;
  if (n != 1) {
    concat_word += " " + ngram_words[n-1];
    temp_map[concat_word] += 1;

  } else {
    temp_map[""] += 1;
  }
}


void count_ngram(char *fname, int N, MapType &counter) {
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


void print_content(MapType temp, char *fout) {
  ofstream os_fout(fout);
  for (auto i = temp.begin(); i != temp.end(); i++) {
    os_fout << i->first << " " << i->second  << endl;
  }
}


int main (int argc, char* argv[])
{
  MapType Ngram_counter;
  char *fname = (char *)"../data/wiki-en-train.word";
  char *fout = (char *)"model.txt";
  int N = 2;

  for (int i = 0; i < argc; i++) {
    string a(argv[i]);
    if (a == "-n") N = atoi(argv[i+1]);
    else if (a == "-f") fname = argv[i+1];
    else if (a == "-o") fout = argv[i+1];
  }
  cout << N << endl; 
  count_ngram((char *)fname, N, Ngram_counter);
  print_content(Ngram_counter, fout);

  return 0;
}
