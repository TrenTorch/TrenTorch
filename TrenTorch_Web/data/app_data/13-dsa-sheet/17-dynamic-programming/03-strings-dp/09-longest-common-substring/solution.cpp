#include <bits/stdc++.h>
using namespace std;

// O(|a| + |b|) time, O(|a|) states with 26 transitions each (suffix automaton)
long long longestCommonSubstring(string a, string b) {
    vector<array<int, 26>> nxt;
    vector<int> link, length;
    array<int, 26> empty;
    empty.fill(-1);
    nxt.push_back(empty);
    link.push_back(-1);
    length.push_back(0);
    int last = 0;
    for (char c : a) {
        int ch = c - 'a';
        int cur = nxt.size();
        nxt.push_back(empty);
        length.push_back(length[last] + 1);
        link.push_back(0);
        int p = last;
        while (p != -1 && nxt[p][ch] == -1) {
            nxt[p][ch] = cur;
            p = link[p];
        }
        if (p != -1) {
            int q = nxt[p][ch];
            if (length[p] + 1 == length[q]) {
                link[cur] = q;
            } else {
                int clone = nxt.size();
                array<int, 26> copy = nxt[q];
                nxt.push_back(copy);
                length.push_back(length[p] + 1);
                link.push_back(link[q]);
                while (p != -1 && nxt[p][ch] == q) {
                    nxt[p][ch] = clone;
                    p = link[p];
                }
                link[q] = clone;
                link[cur] = clone;
            }
        }
        last = cur;
    }

    int best = 0, match = 0, state = 0;
    for (char c : b) {
        int ch = c - 'a';
        while (state && nxt[state][ch] == -1) {
            state = link[state];
            match = length[state];
        }
        if (nxt[state][ch] != -1) {
            state = nxt[state][ch];
            match++;
        } else {
            state = match = 0;
        }
        best = max(best, match);
    }
    return best;
}

int main() {
    cout << longestCommonSubstring("abcdxyz", "xyzabcd") << endl;
    return 0;
}
