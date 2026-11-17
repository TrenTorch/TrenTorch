#include <bits/stdc++.h>
using namespace std;

// O(|s| * |p|) time, O(|p|) space
bool isMatchWildcard(string s, string p) {
    int m = s.size(), n = p.size();
    vector<bool> prev(n + 1, false), cur(n + 1, false);
    prev[0] = true;
    for (int j = 1; j <= n; ++j) prev[j] = prev[j - 1] && p[j - 1] == '*';
    for (int i = 1; i <= m; ++i) {
        fill(cur.begin(), cur.end(), false);
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '*') cur[j] = cur[j - 1] || prev[j];
            else if (p[j - 1] == '?' || p[j - 1] == s[i - 1]) cur[j] = prev[j - 1];
        }
        swap(prev, cur);
    }
    return prev[n];
}

int main() {
    cout << boolalpha << isMatchWildcard("aa", "*") << endl;
    return 0;
}
