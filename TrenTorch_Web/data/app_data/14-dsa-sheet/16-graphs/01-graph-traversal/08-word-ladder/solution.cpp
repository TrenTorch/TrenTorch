#include <bits/stdc++.h>
using namespace std;

// O(N * L^2) time, O(N * L^2) space (N words, L word length; each word yields L wildcard keys of length L)
long long ladderLength(string begin, string end, vector<string> words) {
    unordered_set<string> allowed(words.begin(), words.end());
    if (!allowed.count(end)) return 0;
    unordered_set<string> pool = allowed;
    pool.insert(begin);
    unordered_map<string, vector<string>> groups;
    for (const string& word : pool) {
        for (size_t i = 0; i < word.size(); i++) {
            groups[word.substr(0, i) + "*" + word.substr(i + 1)].push_back(word);
        }
    }
    unordered_set<string> seen = {begin};
    deque<pair<string, long long>> q;
    q.push_back({begin, 1});
    while (!q.empty()) {
        auto [word, steps] = q.front();
        q.pop_front();
        if (word == end) return steps;
        for (size_t i = 0; i < word.size(); i++) {
            auto it = groups.find(word.substr(0, i) + "*" + word.substr(i + 1));
            if (it == groups.end()) continue;
            for (const string& other : it->second) {
                if (!seen.count(other)) {
                    seen.insert(other);
                    q.push_back({other, steps + 1});
                }
            }
        }
    }
    return 0;
}

int main() {
    cout << ladderLength("hit", "cog", vector<string>{"hot", "dot", "dog", "lot", "log", "cog"}) << endl;
    return 0;
}
