#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n * L) time (L max word length), O(total word length * 26) space
vector<vector<long long>> indexPairs(string text, vector<string> words) {
    vector<array<int, 26>> nxt(1);
    nxt[0].fill(-1);
    vector<bool> isEnd(1, false);
    for (const string& w : words) {
        int node = 0;
        for (char c : w) {
            int id = c - 'a';
            if (nxt[node][id] < 0) {
                nxt[node][id] = static_cast<int>(nxt.size());
                array<int, 26> fresh;
                fresh.fill(-1);
                nxt.push_back(fresh);
                isEnd.push_back(false);
            }
            node = nxt[node][id];
        }
        isEnd[node] = true;
    }
    vector<vector<long long>> out;
    int n = text.size();
    for (int i = 0; i < n; i++) {
        int node = 0;
        for (int j = i; j < n; j++) {
            int nx = nxt[node][text[j] - 'a'];
            if (nx < 0) break;
            node = nx;
            if (isEnd[node]) out.push_back({i, j});
        }
    }
    return out;
}

int main() {
    cout << indexPairs("thestoryofleetcodeandme", vector<string>{"story", "fleet", "leetcode"}) << endl;
    return 0;
}
