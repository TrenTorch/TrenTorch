#include <bits/stdc++.h>
using namespace std;

// O(C + N * L) time for the edge scan, plus O(C^2) for the topological sort, where
// N = number of words, L = longest word, C = distinct letters; O(C + E) space
string alienOrder(vector<string> words) {
    set<char> letters;
    for (const string& w : words) {
        for (char ch : w) letters.insert(ch);
    }
    set<pair<char, char>> edges;
    for (size_t i = 0; i + 1 < words.size(); i++) {
        const string& a = words[i];
        const string& b = words[i + 1];
        bool found = false;
        size_t common = min(a.size(), b.size());
        for (size_t j = 0; j < common; j++) {
            if (a[j] != b[j]) {
                edges.insert({a[j], b[j]});
                found = true;
                break;
            }
        }
        if (!found && a.size() > b.size()) return "";
    }
    map<char, vector<char>> adj;
    map<char, int> inDegree;
    for (char ch : letters) {
        adj[ch] = {};
        inDegree[ch] = 0;
    }
    for (const auto& e : edges) {
        adj[e.first].push_back(e.second);
        inDegree[e.second]++;
    }
    priority_queue<char, vector<char>, greater<char>> heap;
    for (char ch : letters) {
        if (inDegree[ch] == 0) heap.push(ch);
    }
    string out;
    while (!heap.empty()) {
        char ch = heap.top();
        heap.pop();
        out.push_back(ch);
        for (char nxt : adj[ch]) {
            inDegree[nxt]--;
            if (inDegree[nxt] == 0) heap.push(nxt);
        }
    }
    return out.size() == letters.size() ? out : "";
}

int main() {
    cout << alienOrder(vector<string>{"wrt", "wrf", "er", "ett", "rftt"}) << endl;
    return 0;
}
