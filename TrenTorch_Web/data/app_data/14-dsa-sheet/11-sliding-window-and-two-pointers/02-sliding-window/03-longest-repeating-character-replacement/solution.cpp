#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (fixed 256-entry count table)
long long characterReplacement(string s, long long k) {
    vector<long long> count(256, 0);
    long long n = s.size();
    long long left = 0;
    long long max_count = 0;
    for (long long right = 0; right < n; right++) {
        unsigned char ch = (unsigned char)s[right];
        count[ch]++;
        max_count = max(max_count, count[ch]);
        if (right - left + 1 - max_count > k) {
            count[(unsigned char)s[left]]--;
            left++;
        }
    }
    return n - left;
}

int main() {
    cout << characterReplacement("AABABBA", 1) << endl;
    return 0;
}
