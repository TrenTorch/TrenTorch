#include <bits/stdc++.h>
using namespace std;

// O(sqrt(n)) time, O(1) space
long long sumDivisorCounts(long long n) {
    long long r = (long long)sqrtl((long double)n);
    while (r * r > n) r--;
    while ((r + 1) * (r + 1) <= n) r++;
    long long s = 0;
    for (long long j = 1; j <= r; j++) s += n / j;
    return 2 * s - r * r;
}

int main() {
    cout << sumDivisorCounts(5) << endl;
    return 0;
}
