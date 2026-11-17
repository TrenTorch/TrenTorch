#include <bits/stdc++.h>
using namespace std;

// O(sqrt(n)) time, O(1) space
long long countDivisors(long long n) {
    long long count = 0;
    for (long long d = 1; d * d <= n; d++) {
        if (n % d == 0) count += (d * d == n) ? 1 : 2;
    }
    return count;
}

int main() {
    cout << countDivisors(36) << endl;
    return 0;
}
