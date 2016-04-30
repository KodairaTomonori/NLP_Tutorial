#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <math.h>
#include <fstream>

using namespace std;

vector<string> split(string &sentence, char delimiter) {
  vector<string> word_list;
  string temp_word;
  stringstream ss(sentence);
  while (getline(ss, temp_word, delimiter)) {
      word_list.push_back(temp_word);
  }
  return word_list;
}

string join(vector<string> &word_list, char delimiter) {
  string str;
  for (auto itr = word_list.begin(); itr != word_list.end(); itr++) {
    str += *itr + delimiter;
    
  } str.pop_back();

  return str;
}

int add_and_abs(int x, int y) {
  return abs(x + y);
} 

int main(int argc, char *argv[]){
  cout << "output Hello World" << endl;
  cout << "Helo World" << endl << endl;

  cout << "test" << endl;
  int my_int = 4;
  float my_float = 2.5;
  string my_string = "hello";
  cout << "string: " << my_string << " float: " << my_float << " int: " << my_int << endl << endl;;
  
  cout << "if/else for" << endl;
  int my_variable = 5;
  if (my_variable == 4) {
    cout << "my_variable is 4" << endl;
  } else {
    cout << "my_variable is not 4" << endl;
  } cout << endl;
  
  for (int i = 0; i < my_variable; i++) {
    cout << "i == " << i << "; ";
  } cout << endl << endl;
  
  cout << "dynamic array";
  vector<int> my_list{1, 2, 4, 8, 16};
  my_list.push_back(32);
  cout << "my_list length: " << my_list.size() << endl;
  cout << "my_list[3]: " << my_list[3] << endl;

  for (auto value = my_list.begin(); value != my_list.end(); value ++) {
    cout << *value << ' ';
  } cout << endl << endl;
  
  cout << "associative array" << endl;
  unordered_map<string, int> my_dict = {{"alan", 22}, {"bill", 45}, {"chris", 17}, {"dan", 27}};
  my_dict["eric"] = 33;
  cout << "my_dict size: " << my_dict.size() << endl;
  cout << "\"chris\": " << my_dict["chris"] << endl;
  for (auto itr = my_dict.begin(); itr != my_dict.end(); itr++) {
    cout << itr->first << ": " << itr->second << endl;
  } cout << endl;

  cout << "string split and join" << endl;
  string sentence = "this is a pen";
  vector<string> word_list = split(sentence, ' ');
  cout << "split by space: ";
  for (auto itr = word_list.begin(); itr != word_list.end(); itr++) {
    cout << *itr << ' ';
  } cout << endl;

  cout << "join with -: ";
  string new_sent = join(word_list, '-');
  cout << new_sent << endl << endl;

  cout << "test function" << endl;
  cout << "|5 - 10| = " << add_and_abs(5, -10) << endl << endl;
  
  cout << "command line arguments" << endl;
  string line, one;
  unordered_map<string, int> counter;
  if (argc > 1) { 
    cout << argv[1] << endl;
    ifstream ifs(argv[1]); 
    if (!ifs) { cout << "file not found" << endl; }
    else {
      while (getline(ifs, line, '\n')) {
        stringstream ss_line(line);
        while (getline(ss_line, one, ' ')) {
          counter[one] += 1;
        }
      }
    }
    for (auto itr = counter.begin(); itr != counter.end(); itr++) {
      cout << itr->first << ": " << itr->second << endl;
    }
  }



  return 0;
}
