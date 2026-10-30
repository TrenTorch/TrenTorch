#include <bits/stdc++.h>
using namespace std;

// Integer square root: largest r with r * r <= x (x >= 0)
long long isqrtLL(long long x) {
    long long r = (long long)sqrtl((long double)x);
    while (r * r > x) r--;
    while ((r + 1) * (r + 1) <= x) r++;
    return r;
}

bool isPerfectSquare(long long x) {
    long long r = isqrtLL(x);
    return r * r == x;
}

// O(sqrt(n)) time, O(1) space
long long numSquares(long long n) {
    if (n == 0) return 0;
    if (isPerfectSquare(n)) return 1;
    long long m = n;
    while (m % 4 == 0) m /= 4;
    if (m % 8 == 7) return 4;
    for (long long i = 1; i * i <= n; i++) {
        if (isPerfectSquare(n - i * i)) return 2;
    }
    return 3;
}

int main() {
    cout << numSquares(12) << endl;
    return 0;
}
