#include <bits/stdc++.h>
using namespace std;

// O(|s| * |t|) time, O(|t|) space
long long numDistinct(string s, string t) {
    const long long mod = 1000000007LL;
    int m = t.size();
    vector<long long> row(m + 1, 0);
    row[0] = 1;
    for (char ch : s) {
        for (int j = m; j >= 1; --j) {
            if (t[j - 1] == ch) row[j] = (row[j] + row[j - 1]) % mod;
        }
    }
    return row[m];
}

int main() {
    cout << numDistinct("rabbbit", "rabbit") << endl;
    return 0;
}
