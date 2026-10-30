#include <bits/stdc++.h>
using namespace std;

static const long long MOD_FIB = 1000000007LL;

// Returns (F(k), F(k+1)) modulo MOD_FIB using fast doubling
static pair<long long, long long> fibPair(long long k) {
    if (k == 0) return {0, 1};
    auto [a, b] = fibPair(k / 2);
    long long c = a * (((2 * b - a) % MOD_FIB + MOD_FIB) % MOD_FIB) % MOD_FIB;
    long long e = (a * a % MOD_FIB + b * b % MOD_FIB) % MOD_FIB;
    if (k % 2) return {e, (c + e) % MOD_FIB};
    return {c, e};
}

// O(log n) time, O(log n) space (recursion depth)
long long fibMod(long long n) {
    return fibPair(n).first;
}

int main() {
    cout << fibMod(10) << endl;
    return 0;
}
