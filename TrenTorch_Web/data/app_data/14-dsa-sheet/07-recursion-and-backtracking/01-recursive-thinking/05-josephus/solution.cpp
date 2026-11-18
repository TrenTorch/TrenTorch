#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long josephus(long long n, long long k) {
    long long position = 0;
    for (long long m = 2; m <= n; m++) {
        position = (position + k) % m;
    }
    return position + 1;
}

int main() {
    cout << josephus(5, 2) << endl;
    return 0;
}
