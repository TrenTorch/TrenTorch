#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (fixed 26-entry tables)
bool checkInclusion(string s1, string s2) {
    long long m = s1.size();
    long long n = s2.size();
    if (m > n) {
        return false;
    }
    vector<long long> need(26, 0), window(26, 0);
    for (char ch : s1) {
        need[ch - 'a']++;
    }
    for (long long i = 0; i < n; i++) {
        window[s2[i] - 'a']++;
        if (i >= m) {
            window[s2[i - m] - 'a']--;
        }
        if (i >= m - 1 && window == need) {
            return true;
        }
    }
    return m == 0;
}

int main() {
    cout << boolalpha << checkInclusion("ab", "eidbaooo") << endl;
    return 0;
}
