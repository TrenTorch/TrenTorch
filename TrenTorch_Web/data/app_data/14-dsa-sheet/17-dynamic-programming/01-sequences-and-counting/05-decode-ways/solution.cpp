#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long numDecodings(string s) {
    const long long mod = 1000000007LL;
    long long a = 1, b = 1;
    for (size_t i = 1; i <= s.size(); i++) {
        long long now = 0;
        if (s[i - 1] != '0') now += b;
        if (i >= 2) {
            string sub = s.substr(i - 2, 2);
            if (sub >= "10" && sub <= "26") now += a;
        }
        a = b;
        b = now % mod;
    }
    return s.empty() ? 0 : b;
}

int main() {
    cout << numDecodings("12") << endl;
    return 0;
}
