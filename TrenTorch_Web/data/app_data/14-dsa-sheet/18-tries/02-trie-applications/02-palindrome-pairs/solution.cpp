#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

static string reversedCopy(const string& s) {
    return string(s.rbegin(), s.rend());
}

static bool isPalindrome(const string& s) {
    return reversedCopy(s) == s;
}

// O(n * L^2) time (L max word length, cut and substring work), O(n * L) space
vector<vector<long long>> palindromePairs(vector<string> words) {
    map<string, vector<int>> index;
    int n = words.size();
    for (int i = 0; i < n; i++) index[words[i]].push_back(i);
    set<pair<int, int>> found;
    for (int i = 0; i < n; i++) {
        const string& w = words[i];
        for (size_t cut = 0; cut <= w.size(); cut++) {
            string prefix = w.substr(0, cut);
            string suffix = w.substr(cut);
            if (isPalindrome(prefix)) {
                auto it = index.find(reversedCopy(suffix));
                if (it != index.end()) {
                    for (int j : it->second) {
                        if (j != i) found.insert({j, i});
                    }
                }
            }
            if (isPalindrome(suffix)) {
                auto it = index.find(reversedCopy(prefix));
                if (it != index.end()) {
                    for (int j : it->second) {
                        if (j != i) found.insert({i, j});
                    }
                }
            }
        }
    }
    vector<vector<long long>> out;
    for (const auto& p : found) out.push_back({p.first, p.second});
    return out;
}

int main() {
    cout << palindromePairs(vector<string>{"abcd", "dcba", "lls", "s", "sssll"}) << endl;
    return 0;
}
