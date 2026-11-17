#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n * L log L + G log G) time (L = word length, G = groups), O(n * L) space
vector<vector<string>> groupAnagrams(vector<string> words) {
    map<string, vector<string>> groups;
    for (const string& word : words) {
        string key = word;
        sort(key.begin(), key.end());
        groups[key].push_back(word);
    }
    vector<vector<string>> out;
    for (auto& [key, group] : groups) {
        sort(group.begin(), group.end());
        out.push_back(group);
    }
    sort(out.begin(), out.end());
    return out;
}

int main() {
    cout << groupAnagrams(vector<string>{"eat", "tea", "tan", "ate", "nat", "bat"}) << endl;
    return 0;
}
