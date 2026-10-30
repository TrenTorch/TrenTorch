#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space
long long longestPalindromeSubseq(string s) {
    int n = s.size();
    if (n == 0) return 0;
    vector<long long> prev(n, 0), cur(n, 0);
    for (int i = n - 1; i >= 0; --i) {
        fill(cur.begin(), cur.end(), 0);
        cur[i] = 1;
        for (int j = i + 1; j < n; ++j) {
            if (s[i] == s[j]) cur[j] = 2 + prev[j - 1];
            else cur[j] = max(prev[j], cur[j - 1]);
        }
        swap(prev, cur);
    }
    return prev[n - 1];
}

int main() {
    cout << longestPalindromeSubseq("bbbab") << endl;
    return 0;
}
