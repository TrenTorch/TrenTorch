#include <bits/stdc++.h>
using namespace std;

// O(total word length + n * L) time, where L is the longest word, O(total word length + n) space
bool wordBreak(string s, vector<string> words) {
    struct Node {
        unordered_map<char, int> next;
        bool end = false;
    };
    vector<Node> trie(1);
    for (const string& w : words) {
        int node = 0;
        for (char ch : w) {
            auto it = trie[node].next.find(ch);
            if (it == trie[node].next.end()) {
                trie.emplace_back();
                int created = (int)trie.size() - 1;
                trie[node].next[ch] = created;
                node = created;
            } else {
                node = it->second;
            }
        }
        trie[node].end = true;
    }

    size_t n = s.size();
    vector<char> reachable(n + 1, 0);
    reachable[0] = 1;
    for (size_t i = 0; i < n; i++) {
        if (!reachable[i]) continue;
        int node = 0;
        for (size_t j = i; j < n; j++) {
            auto it = trie[node].next.find(s[j]);
            if (it == trie[node].next.end()) break;
            node = it->second;
            if (trie[node].end) reachable[j + 1] = 1;
        }
    }
    return reachable[n] != 0;
}

int main() {
    cout << boolalpha << wordBreak("leetcode", vector<string>{"leet", "code"}) << endl;
    return 0;
}
