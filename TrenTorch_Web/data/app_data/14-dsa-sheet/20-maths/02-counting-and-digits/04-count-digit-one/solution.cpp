#include <bits/stdc++.h>
using namespace std;

// O(log10 n) time, O(1) space
long long countDigitOne(long long n) {
    long long total = 0;
    for (long long p = 1; p <= n; p *= 10) {
        long long high = n / (p * 10);
        long long cur = (n / p) % 10;
        long long low = n % p;
        total += high * p;
        if (cur > 1) total += p;
        else if (cur == 1) total += low + 1;
    }
    return total;
}

int main() {
    cout << countDigitOne(13) << endl;
    return 0;
}
