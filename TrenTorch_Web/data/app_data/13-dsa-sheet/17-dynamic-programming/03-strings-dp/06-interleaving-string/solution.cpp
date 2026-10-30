#include <bits/stdc++.h>
using namespace std;

// O(|a| * |b|) time, O(|b|) space
bool isInterleave(string a, string b, string c) {
    int m = a.size(), n = b.size();
    if (m + n != (int)c.size()) return false;
    vector<bool> row(n + 1, false);
    row[0] = true;
    for (int j = 1; j <= n; ++j) row[j] = row[j - 1] && b[j - 1] == c[j - 1];
    for (int i = 1; i <= m; ++i) {
        row[0] = row[0] && a[i - 1] == c[i - 1];
        for (int j = 1; j <= n; ++j) {
            row[j] = (row[j] && a[i - 1] == c[i + j - 1]) || (row[j - 1] && b[j - 1] == c[i + j - 1]);
        }
    }
    return row[n];
}

int main() {
    cout << boolalpha << isInterleave("aabcc", "dbbca", "aadbbcbcac") << endl;
    return 0;
}
