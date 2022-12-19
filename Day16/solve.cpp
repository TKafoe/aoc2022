#include <fstream>
#include <iostream>
#include <unordered_set>
#include <regex>

bool areDisjoint(const std::unordered_set<std::string>& s1, const std::unordered_set<std::string>& s2) {
  for (const auto& el1 : s1) {
    if (s2.contains(el1)) {
      return false;
    }
  }
  return true;
}

int task(int v1, int v2, const std::unordered_set<std::string>& s1, const std::unordered_set<std::string>& s2) {
  if (areDisjoint(s1, s2)) {
    return v1 + v2;
  }
  return 0;
}

int main() {
    std::ifstream f1("/home/tkafoe/Files/Projects/AdventOfCode/Day16/input_dump.txt");

    std::regex exp("([A-Z][A-Z])");
    std::regex exp2("(\\d+)");
    std::smatch sm;
    std::smatch sm2;
    std::string line;
    std::vector<std::pair<int, std::unordered_set<std::string>>> data;
    while (std::getline(f1, line)){
      regex_search(line, sm2, exp2);
      int val = std::stoi(sm2[0]);
      std::unordered_set<std::string> s;
      bool skip = true;
      while (regex_search(line, sm, exp)) {
        if (skip) {
          skip = false;
        } else {
          s.insert(sm[0]);
        }
        line = sm.suffix();
      }
      data.emplace_back(val, s);
    }
    std::cout << "Reading done" << std::endl;
    int mx = 0;
    std::unordered_set<std::string> maxpath1;
    std::unordered_set<std::string> maxpath2;
    #pragma omp parallel for
    for (int i = 0; i < data.size(); i++) {
      for (int j = i; j < data.size(); j++) {
        if (data[i].first + data[j].first <= mx) {
          continue;
        }
        int val = task(data[i].first, data[j].first, data[i].second, data[j].second);
        if (val > mx) {
          mx = val;
          maxpath1 = data[i].second;
          maxpath2 = data[j].second;
        }
      }
    }

    std::cout << mx << std::endl;
    for (auto i : maxpath1) {
      std::cout << i << ", ";
    }
    std::cout << std::endl;
    for (auto i : maxpath2) {
      std::cout << i << ", ";
    }
    std::cout << std::endl;

	return 0;
}
