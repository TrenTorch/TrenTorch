#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string reverseWords(string s) {
    istringstream iss(s);
    vector<string> words;
    string word;
    while (iss >> word) {
        words.push_back(word);
    }
    string out;
    for (size_t i = words.size(); i-- > 0;) {
        out += words[i];
        if (i > 0) {
            out += ' ';
        }
    }
    return out;
}

int main() {
    cout << reverseWords("the sky is blue") << endl;
    return 0;
}
