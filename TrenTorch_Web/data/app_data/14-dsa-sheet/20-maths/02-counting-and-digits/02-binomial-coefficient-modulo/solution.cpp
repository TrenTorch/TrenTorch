#include <bits/stdc++.h>
using namespace std;

// O(k log MOD) time, O(1) space (multiplicative formula with Fermat inverse)
long long binomialMod(long long n, long long k) {
    const long long MOD = 1000000007LL;
    if (k < 0 || k > n) return 0;
    k = min(k, n - k);
    long long num = 1, den = 1;
    for (long long i = 0; i < k; i++) {
        num = num * ((n - i) % MOD) % MOD;
        den = den * ((i + 1) % MOD) % MOD;
    }
    long long e = MOD - 2, base = den, inv = 1;
    while (e > 0) {
        if (e & 1) inv = inv * base % MOD;
        base = base * base % MOD;
        e >>= 1;
    }
    return num * inv % MOD;
}

int main() {
    cout << binomialMod(5, 2) << endl;
    return 0;
}
