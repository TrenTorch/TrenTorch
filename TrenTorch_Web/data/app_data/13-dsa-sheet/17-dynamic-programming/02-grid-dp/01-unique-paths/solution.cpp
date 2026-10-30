#include <bits/stdc++.h>
using namespace std;

long long modPow(long long base, long long exp, long long mod) {
    long long result = 1 % mod;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

// O(rows + cols) time, O(rows + cols) space (factorials modulo a prime)
long long uniquePaths(long long rows, long long cols) {
    const long long mod = 1000000007LL;
    long long n = rows + cols - 2;
    long long k = rows - 1;
    vector<long long> fact(n + 1, 1);
    for (long long i = 1; i <= n; i++) {
        fact[i] = fact[i - 1] * i % mod;
    }
    long long denom = fact[k] * fact[n - k] % mod;
    return fact[n] * modPow(denom, mod - 2, mod) % mod;
}

int main() {
    cout << uniquePaths(3, 7) << endl;
    return 0;
}
