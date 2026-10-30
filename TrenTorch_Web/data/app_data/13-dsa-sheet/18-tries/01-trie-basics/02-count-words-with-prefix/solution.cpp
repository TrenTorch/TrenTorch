#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(total word length + total query length) time, O(total word length * 26) space
vector<long long> countWithPrefix(vector<string> words, vector<string> queries) {
    vector<array<int, 26>> nxt(1);
    nxt[0].fill(-1);
    vector<long long> cnt(1, 0);
    for (const string& w : words) {
        int node = 0;
        for (char c : w) {
            int id = c - 'a';
            if (nxt[node][id] < 0) {
                nxt[node][id] = static_cast<int>(nxt.size());
                array<int, 26> fresh;
                fresh.fill(-1);
                nxt.push_back(fresh);
                cnt.push_back(0);
            }
            node = nxt[node][id];
            cnt[node]++;
        }
    }
    vector<long long> out;
    for (const string& q : queries) {
        int node = 0;
        bool ok = true;
        for (char c : q) {
            int nx = nxt[node][c - 'a'];
            if (nx < 0) {
                ok = false;
                break;
            }
            node = nx;
        }
        out.push_back(ok ? cnt[node] : 0);
    }
    return out;
}

int main() {
    cout << countWithPrefix(vector<string>{"apple", "app", "apt", "bat"}, vector<string>{"ap", "app", "b", "c"}) << endl;
    return 0;
}
