#include <bits/stdc++.h>
using namespace std;

// O(log exp) time, O(1) space
long long powerMod(long long base, long long exp, long long mod) {
    long long result = 1 % mod;
    base %= mod;
    while (exp) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

int main() {
    cout << powerMod(2, 10, 1000) << endl;
    return 0;
}
