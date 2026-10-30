#include <bits/stdc++.h>
using namespace std;

// O(n * L log n) time (n words, L max length), O(n * L) space
string longestWord(vector<string> words) {
    set<string> uniq(words.begin(), words.end());
    map<size_t, vector<string>> byLength;
    for (const string& w : uniq) byLength[w.size()].push_back(w);
    set<string> built = {""};
    string best = "";
    for (size_t length = 1;; length++) {
        auto it = byLength.find(length);
        if (it == byLength.end()) return best;
        vector<string> good;
        for (const string& w : it->second) {
            if (built.count(w.substr(0, w.size() - 1))) good.push_back(w);
        }
        if (good.empty()) return best;
        for (const string& w : good) built.insert(w);
        best = *min_element(good.begin(), good.end());
    }
}

int main() {
    cout << longestWord(vector<string>{"w", "wo", "wor", "worl", "world"}) << endl;
    return 0;
}
