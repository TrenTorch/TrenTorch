#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
bool wordPattern(string pattern, vector<string> words) {
    if (pattern.size() != words.size()) return false;
    unordered_map<char, string> letterToWord;
    unordered_map<string, char> wordToLetter;
    for (size_t i = 0; i < pattern.size(); i++) {
        char letter = pattern[i];
        const string& word = words[i];
        auto lw = letterToWord.emplace(letter, word);
        if (lw.first->second != word) return false;
        auto wl = wordToLetter.emplace(word, letter);
        if (wl.first->second != letter) return false;
    }
    return true;
}

int main() {
    cout << boolalpha << wordPattern("abba", vector<string>{"dog", "cat", "cat", "dog"}) << endl;
    return 0;
}
