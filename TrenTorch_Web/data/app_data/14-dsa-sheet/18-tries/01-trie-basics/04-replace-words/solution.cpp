#include <bits/stdc++.h>
using namespace std;

// O(total root length * 26 + sentence length) time, O(total root length * 26) space
string replaceWords(vector<string> roots, string sentence) {
    vector<array<int, 26>> nxt(1);
    nxt[0].fill(-1);
    vector<bool> isEnd(1, false);
    for (const string& r : roots) {
        int node = 0;
        for (char c : r) {
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
    istringstream iss(sentence);
    string word;
    string result;
    bool first = true;
    while (iss >> word) {
        string out = word;
        int node = 0;
        for (size_t i = 0; i < word.size(); i++) {
            int nx = nxt[node][word[i] - 'a'];
            if (nx < 0) break;
            node = nx;
            if (isEnd[node]) {
                out = word.substr(0, i + 1);
                break;
            }
        }
        if (!first) result += ' ';
        result += out;
        first = false;
    }
    return result;
}

int main() {
    cout << replaceWords(vector<string>{"cat", "bat", "rat"}, "the cattle was rattled by the battery") << endl;
    return 0;
}
