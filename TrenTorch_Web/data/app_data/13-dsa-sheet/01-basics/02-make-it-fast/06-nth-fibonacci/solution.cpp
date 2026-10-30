#include <bits/stdc++.h>
using namespace std;

// Returns (F(k), F(k+1)) modulo 2^64 using fast doubling.
// Unsigned arithmetic wraps well-defined; exact for k <= 92 (F(92) is the largest that fits in 64 bits).
static pair<unsigned long long, unsigned long long> fibPair(unsigned long long k) {
    if (k == 0) return {0ULL, 1ULL};
    auto [a, b] = fibPair(k >> 1);
    unsigned long long c = a * (2ULL * b - a);
    unsigned long long d = a * a + b * b;
    if (k & 1ULL) return {d, c + d};
    return {c, d};
}

// O(log n) time, O(log n) space (recursion depth)
long long nthFibonacci(long long n) {
    return (long long)fibPair((unsigned long long)n).first;
}

int main() {
    cout << nthFibonacci(10) << endl;
    return 0;
}
