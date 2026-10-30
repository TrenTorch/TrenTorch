#include <bits/stdc++.h>
using namespace std;

// O(sqrt(n)) time, O(1) space (trial division over prime factors)
long long eulerPhi(long long n) {
    long long result = n;
    long long d = 2;
    while (d * d <= n) {
        if (n % d == 0) {
            while (n % d == 0) n /= d;
            result -= result / d;
        }
        d += (d == 2) ? 1 : 2;
    }
    if (n > 1) result -= result / n;
    return result;
}

int main() {
    cout << eulerPhi(12) << endl;
    return 0;
}
