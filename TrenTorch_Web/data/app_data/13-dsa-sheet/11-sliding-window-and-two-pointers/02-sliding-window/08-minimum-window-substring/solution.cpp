#include <bits/stdc++.h>
using namespace std;

// O(|s| + |t|) time, O(|s| + |t|) space (character maps)
string minWindow(string s, string t) {
    if (t.empty()) {
        return "";
    }
    long long n = s.size();
    map<char, long long> need, have;
    for (char ch : t) {
        need[ch]++;
    }
    long long missing = need.size();
    long long best_start = 0;
    long long best_len = n + 1;
    long long left = 0;
    for (long long right = 0; right < n; right++) {
        char ch = s[right];
        have[ch]++;
        if (need.count(ch) && have[ch] == need[ch]) {
            missing--;
        }
        while (missing == 0) {
            if (right - left + 1 < best_len) {
                best_start = left;
                best_len = right - left + 1;
            }
            char gone = s[left];
            have[gone]--;
            if (need.count(gone) && have[gone] < need[gone]) {
                missing++;
            }
            left++;
        }
    }
    return best_len <= n ? s.substr(best_start, best_len) : "";
}

int main() {
    cout << minWindow("ADOBECODEBANC", "ABC") << endl;
    return 0;
}
