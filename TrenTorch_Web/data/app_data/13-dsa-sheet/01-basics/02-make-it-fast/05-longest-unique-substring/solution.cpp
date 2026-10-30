#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (sliding window over 256 byte values)
long long longestUniqueSubstring(string s) {
    vector<long long> last(256, -1);
    long long start = 0;
    long long best = 0;
    for (long long i = 0; i < (long long)s.size(); i++) {
        unsigned char ch = (unsigned char)s[i];
        if (last[ch] >= start) start = last[ch] + 1;
        last[ch] = i;
        best = max(best, i - start + 1);
    }
    return best;
}

int main() {
    cout << longestUniqueSubstring("abcabcbb") << endl;
    return 0;
}
