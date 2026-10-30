#include <bits/stdc++.h>
using namespace std;

// O(n log log n) time, O(n) space (sieve of Eratosthenes)
long long countPrimes(long long n) {
    if (n < 3) return 0;
    vector<char> sieve(n, 1);
    sieve[0] = sieve[1] = 0;
    for (long long i = 2; i * i < n; i++) {
        if (sieve[i]) {
            for (long long j = i * i; j < n; j += i) sieve[j] = 0;
        }
    }
    long long total = 0;
    for (char c : sieve) total += c;
    return total;
}

int main() {
    cout << countPrimes(10) << endl;
    return 0;
}
