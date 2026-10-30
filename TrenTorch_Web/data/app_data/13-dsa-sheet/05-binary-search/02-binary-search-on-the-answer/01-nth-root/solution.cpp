#include <bits/stdc++.h>
using namespace std;

// Number of bits needed to write n (n >= 1)
long long bitLength(long long n) {
    long long bits = 0;
    while (n > 0) {
        n >>= 1;
        bits++;
    }
    return bits;
}

// Returns base^m if it is at most n; otherwise returns n + 1 (any value above n).
// Avoids overflow: result * base > n exactly when result > n / base (integer division).
long long powerAtMost(long long base, long long m, long long n) {
    long long result = 1;
    for (long long i = 0; i < m; i++) {
        if (result > n / base) return n + 1;
        result *= base;
    }
    return result;
}

// O(log n) time (binary search over at most 2^31 candidates times m steps), O(1) space
long long nthRoot(long long n, long long m) {
    long long lo = 1, hi = 1LL << (bitLength(n) / m + 1);
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        long long power = powerAtMost(mid, m, n);
        if (power == n) return mid;
        if (power < n) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

int main() {
    cout << nthRoot(27, 3) << endl;
    return 0;
}
