#include <bits/stdc++.h>
using namespace std;

// O(log_5 n) time, O(1) space (Legendre's formula for the power of 5)
long long trailingZeros(long long n) {
    long long count = 0;
    while (n) {
        n /= 5;
        count += n;
    }
    return count;
}

int main() {
    cout << trailingZeros(25) << endl;
    return 0;
}
