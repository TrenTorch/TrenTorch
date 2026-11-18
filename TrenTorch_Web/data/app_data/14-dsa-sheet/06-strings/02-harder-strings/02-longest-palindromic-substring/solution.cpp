#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string longestPalindromicSubstring(string s) {
    string t = "#";
    for (char c : s) {
        t += c;
        t += '#';
    }
    long long n = t.size();
    vector<long long> radius(n, 0);
    long long centre = 0, right = 0;
    long long best_len = 0, best_centre = 0;
    for (long long i = 0; i < n; i++) {
        if (i < right) radius[i] = min(right - i, radius[2 * centre - i]);
        while (i - radius[i] - 1 >= 0 && i + radius[i] + 1 < n &&
               t[i - radius[i] - 1] == t[i + radius[i] + 1]) {
            radius[i]++;
        }
        if (i + radius[i] > right) {
            centre = i;
            right = i + radius[i];
        }
        if (radius[i] > best_len) {
            best_len = radius[i];
            best_centre = i;
        }
    }
    long long start = (best_centre - best_len) / 2;
    return s.substr(start, best_len);
}

int main() {
    cout << longestPalindromicSubstring("babad") << endl;
    return 0;
}
