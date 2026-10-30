#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space
long long minCutPalindromes(string s) {
    int n = s.size();
    if (n == 0) return 0;
    // cuts[i]: fewest cuts for the first i letters
    vector<long long> cuts(n + 1);
    for (int i = 0; i <= n; ++i) cuts[i] = i - 1;
    for (int centre = 0; centre < n; ++centre) {
        for (int pass = 0; pass < 2; ++pass) {
            int left = centre, right = centre + pass;
            while (left >= 0 && right < n && s[left] == s[right]) {
                if (cuts[left] + 1 < cuts[right + 1]) cuts[right + 1] = cuts[left] + 1;
                left--;
                right++;
            }
        }
    }
    return cuts[n];
}

int main() {
    cout << minCutPalindromes("aab") << endl;
    return 0;
}
