#include <bits/stdc++.h>
using namespace std;

// KMP: O(n + m) time, O(m) space
long long findNeedle(string haystack, string needle) {
    if (needle.empty()) return 0;
    int m = needle.size();
    vector<int> fail(m, 0);
    int k = 0;
    for (int i = 1; i < m; i++) {
        while (k > 0 && needle[i] != needle[k]) k = fail[k - 1];
        if (needle[i] == needle[k]) k++;
        fail[i] = k;
    }
    k = 0;
    int n = haystack.size();
    for (int i = 0; i < n; i++) {
        while (k > 0 && haystack[i] != needle[k]) k = fail[k - 1];
        if (haystack[i] == needle[k]) k++;
        if (k == m) return i - k + 1;
    }
    return -1;
}

int main() {
    cout << findNeedle("sadbutsad", "sad") << endl;
    return 0;
}
