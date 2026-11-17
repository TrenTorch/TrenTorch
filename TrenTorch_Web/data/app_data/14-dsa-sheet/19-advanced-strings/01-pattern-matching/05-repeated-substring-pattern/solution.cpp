#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space (prefix function)
bool repeatedSubstringPattern(string s) {
    int n = s.size();
    if (n < 2) return false;
    vector<int> pi(n, 0);
    int k = 0;
    for (int i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    int period = n - pi[n - 1];
    return pi[n - 1] > 0 && n % period == 0;
}

int main() {
    cout << boolalpha << repeatedSubstringPattern("abab") << endl;
    return 0;
}
