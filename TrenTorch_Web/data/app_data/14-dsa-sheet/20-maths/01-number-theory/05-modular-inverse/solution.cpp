#include <bits/stdc++.h>
using namespace std;

// O(log m) time, O(1) space (extended Euclidean algorithm)
long long modInverse(long long a, long long m) {
    if (m == 1) return 0;
    long long old_r = a % m, r = m;
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
    if (old_r != 1) return -1;
    return ((old_x % m) + m) % m;
}

int main() {
    cout << modInverse(3, 11) << endl;
    return 0;
}
