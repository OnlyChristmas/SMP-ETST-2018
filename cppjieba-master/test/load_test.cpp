#include <iostream>
#include <ctime>
#include <fstream>
#include <sstream>
#include <iterator>
#include <vector>
#include "cppjieba/MPSegment.hpp"
#include "cppjieba/HMMSegment.hpp"
#include "cppjieba/MixSegment.hpp"
#include "cppjieba/KeywordExtractor.hpp"
#include "limonp/Colors.hpp"

using namespace cppjieba;

int main(int argc, char **argv) {
  char* input_path = NULL;
  char* output_path = NULL;
  int c = 1;
  while(c < argc){
     std::string arg = argv[c];
     if(arg == "-i"){
	input_path = argv[++c];
     }else if(arg == "-o"){ output_path = argv[++c];
     
     }
     c++;
  }
  MixSegment seg("cppjieba-master/dict/jieba.dict.utf8", "cppjieba-master/dict/hmm_model.utf8");
  vector<string> res;
  string doc;
  ifstream ifs(input_path);
  std::ofstream output_file(output_path);
  assert(ifs);
  string s;
  string results;
  long beginTime = clock();
  while(std::getline(ifs,s))
  {
	  seg.Cut(s, res);
	  string results;

	  const char* const delim = " ";

	  std::ostringstream imploded;
	  std::copy(res.begin(), res.end(), std::ostream_iterator<std::string>(imploded, delim));
	  //results << res;
	  output_file << imploded.str() << endl;
	  res.clear();

  }
  //doc << ifs;
  //long beginTime = clock();
  //res.clear();
  //seg.Cut(doc, res);
  //std::ofstream output_file("./example.txt");
  //std::ostream_iterator<std::string> output_iterator(output_file, "\n");
  //std::copy(res.begin(), res.end(), output_iterator);
    long endTime = clock();
  ColorPrintln(GREEN, "Cut: [%.3lf seconds]time consumed.", double(endTime - beginTime)/CLOCKS_PER_SEC);
}

void Extract(size_t times = 400) {
  KeywordExtractor Extractor("../dict/jieba.dict.utf8", "../dict/hmm_model.utf8", "../dict/idf.utf8", "../dict/stop_words.utf8");
  vector<string> words;
  string doc;
  ifstream ifs("../test/testdata/review.100");
  assert(ifs);
  doc << ifs;
  long beginTime = clock();
  for (size_t i = 0; i < times; i ++) {
    printf("process [%3.0lf %%]\r", 100.0*(i+1)/times);
    fflush(stdout);
    words.clear();
    Extractor.Extract(doc, words, 5);
  }
  printf("\n");
  long endTime = clock();
  ColorPrintln(GREEN, "Extract: [%.3lf seconds]time consumed.", double(endTime - beginTime)/CLOCKS_PER_SEC);
}


