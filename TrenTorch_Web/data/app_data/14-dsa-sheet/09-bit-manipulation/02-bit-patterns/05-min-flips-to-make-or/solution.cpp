#include <bits/stdc++.h>
using namespace std;

// O(1) time (fixed 31 bit positions), O(1) space
long long minFlips(long long a, long long b, long long c) {
    long long flips = 0;
    for (int i = 0; i < 31; i++) {
        long long x = (a >> i) & 1;
        long long y = (b >> i) & 1;
        long long z = (c >> i) & 1;
        if (z == 0) flips += x + y;
        else if (x == 0 && y == 0) flips += 1;
    }
    return flips;
}

int main() {
    cout << minFlips(2, 6, 5) << endl;
    return 0;
}
