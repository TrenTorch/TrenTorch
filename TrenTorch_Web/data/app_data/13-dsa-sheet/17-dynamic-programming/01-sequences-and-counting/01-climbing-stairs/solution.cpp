#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

// returns (F(k), F(k + 1)) modulo MOD, fast doubling
pair<long long, long long> fibPair(long long k) {
    if (k == 0) return {0, 1};
    auto [a, b] = fibPair(k >> 1);
    long long c = a * ((2 * b - a) % MOD + MOD) % MOD;
    long long d = (a * a + b * b) % MOD;
    if (k & 1) return {d, (c + d) % MOD};
    return {c, d};
}

// O(log n) time, O(log n) space (recursion depth)
long long climbStairs(long long n) {
    return fibPair(n + 1).first;
}

int main() {
    cout << climbStairs(3) << endl;
    return 0;
}
