#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string shortestPalindrome(string s) {
    string t = s + "#" + string(s.rbegin(), s.rend());
    long long m = t.size();
    vector<long long> pi(m, 0);
    long long k = 0;
    for (long long i = 1; i < m; i++) {
        while (k && t[i] != t[k]) k = pi[k - 1];
        if (t[i] == t[k]) k++;
        pi[i] = k;
    }
    long long border = m ? pi[m - 1] : 0;
    string rest = s.substr(border);
    reverse(rest.begin(), rest.end());
    return rest + s;
}

int main() {
    cout << shortestPalindrome("aacecaaa") << endl;
    return 0;
}
