#include <bits/stdc++.h>
using namespace std;

// Inverse of a modulo m (gcd(a, m) = 1 assumed); 0 when m == 1
long long modInv(long long a, long long m) {
    if (m == 1) return 0;
    long long old_r = ((a % m) + m) % m, r = m;
    long long old_x = 1, x = 0;
    while (r) {
        long long q = old_r / r;
        long long tmp = old_r - q * r;
        old_r = r;
        r = tmp;
        tmp = old_x - q * x;
        old_x = x;
        x = tmp;
    }
    return ((old_x % m) + m) % m;
}

// O(k log M) time for k congruences (M = lcm bound), O(1) space
long long solveCongruences(vector<long long> remainders, vector<long long> moduli) {
    long long x = 0, modulus = 1;
    for (size_t i = 0; i < remainders.size(); i++) {
        long long r = remainders[i], m = moduli[i];
        long long g = gcd(modulus, m);
        if ((r - x) % g != 0) return -1;
        long long lcm = modulus / g * m;
        long long mg = m / g;
        long long d = (r - x) / g;
        long long t = ((d % mg) + mg) % mg;
        t = t * modInv(modulus / g, mg) % mg;
        x = (x + modulus * t) % lcm;
        modulus = lcm;
    }
    return x;
}

int main() {
    cout << solveCongruences(vector<long long>{2, 3, 2}, vector<long long>{3, 5, 7}) << endl;
    return 0;
}
