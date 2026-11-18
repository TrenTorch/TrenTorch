#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string longestHappyPrefix(string s) {
    long long n = s.size();
    if (n == 0) return "";
    vector<long long> pi(n, 0);
    long long k = 0;
    for (long long i = 1; i < n; i++) {
        while (k && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    return s.substr(0, pi[n - 1]);
}

int main() {
    cout << longestHappyPrefix("level") << endl;
    return 0;
}
