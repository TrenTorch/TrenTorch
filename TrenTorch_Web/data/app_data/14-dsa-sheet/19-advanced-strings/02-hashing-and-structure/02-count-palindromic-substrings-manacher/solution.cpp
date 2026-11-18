#include <bits/stdc++.h>
using namespace std;

// O(n) time (Manacher), O(n) space
long long countPalindromesFast(string s) {
    long long n = s.size();
    long long total = 0;

    vector<long long> d1(n, 0);
    long long left = 0, right = -1;
    for (long long i = 0; i < n; i++) {
        long long k = (i > right) ? 1 : min(d1[left + right - i], right - i + 1);
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        total += k;
        if (i + k - 1 > right) {
            left = i - k + 1;
            right = i + k - 1;
        }
    }

    vector<long long> d2(n, 0);
    left = 0;
    right = -1;
    for (long long i = 0; i < n; i++) {
        long long k = (i > right) ? 0 : min(d2[left + right - i + 1], right - i + 1);
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        total += k;
        if (i + k - 1 > right) {
            left = i - k;
            right = i + k - 1;
        }
    }
    return total;
}

int main() {
    cout << countPalindromesFast("aaa") << endl;
    return 0;
}
