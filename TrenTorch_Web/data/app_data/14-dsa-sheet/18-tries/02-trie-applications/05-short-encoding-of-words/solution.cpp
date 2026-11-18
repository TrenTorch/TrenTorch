#include <bits/stdc++.h>
using namespace std;

// O(total word length * 26) time and space (trie of reversed words)
long long minimumLengthEncoding(vector<string> words) {
    set<string> uniq(words.begin(), words.end());
    vector<array<int, 26>> nxt(1);
    nxt[0].fill(-1);
    vector<pair<int, int>> ends;
    for (const string& w : uniq) {
        int node = 0;
        for (int k = static_cast<int>(w.size()) - 1; k >= 0; k--) {
            int id = w[k] - 'a';
            if (nxt[node][id] < 0) {
                nxt[node][id] = static_cast<int>(nxt.size());
                array<int, 26> fresh;
                fresh.fill(-1);
                nxt.push_back(fresh);
            }
            node = nxt[node][id];
        }
        ends.push_back({node, static_cast<int>(w.size())});
    }
    long long total = 0;
    for (const auto& e : ends) {
        int node = e.first;
        bool leaf = true;
        for (int c = 0; c < 26; c++) {
            if (nxt[node][c] >= 0) {
                leaf = false;
                break;
            }
        }
        if (leaf) total += e.second + 1;
    }
    return total;
}

int main() {
    cout << minimumLengthEncoding(vector<string>{"time", "me", "bell"}) << endl;
    return 0;
}
