#include <bits/stdc++.h>
using namespace std;

// O(|s| * |p|) time, O(|p|) space
bool isMatchRegex(string s, string p) {
    auto fits = [](char x, char ch) { return x == '.' || x == ch; };
    int m = s.size(), n = p.size();
    vector<bool> prev(n + 1, false), cur(n + 1, false);
    prev[0] = true;
    for (int j = 2; j <= n; ++j) prev[j] = p[j - 1] == '*' && prev[j - 2];
    for (int i = 1; i <= m; ++i) {
        fill(cur.begin(), cur.end(), false);
        for (int j = 1; j <= n; ++j) {
            if (p[j - 1] == '*') {
                cur[j] = (j >= 2 && cur[j - 2]) || (j >= 2 && fits(p[j - 2], s[i - 1]) && prev[j]);
            } else {
                cur[j] = fits(p[j - 1], s[i - 1]) && prev[j - 1];
            }
        }
        swap(prev, cur);
    }
    return prev[n];
}

int main() {
    cout << boolalpha << isMatchRegex("aab", "c*a*b") << endl;
    return 0;
}
