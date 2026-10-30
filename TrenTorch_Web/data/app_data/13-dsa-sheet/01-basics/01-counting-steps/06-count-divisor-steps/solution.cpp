#include <bits/stdc++.h>
using namespace std;

// O(sqrt(n)) time, O(1) space
long long countDivisorSteps(long long n) {
    long long total = 0;
    long long i = 1;
    while (i <= n) {
        long long q = n / i;
        long long j = n / q;
        total += q * (j - i + 1);
        i = j + 1;
    }
    return total;
}

int main() {
    cout << countDivisorSteps(5) << endl;
    return 0;
}
