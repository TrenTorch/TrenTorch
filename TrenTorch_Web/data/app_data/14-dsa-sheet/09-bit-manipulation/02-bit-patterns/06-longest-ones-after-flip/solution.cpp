#include <bits/stdc++.h>
using namespace std;

// O(1) time (fixed 32 bit positions), O(1) space
long long longestOnesAfterFlip(long long n) {
    long long best = 0, current = 0, previous = 0;
    for (int i = 0; i < 32; i++) {
        if ((n >> i) & 1) {
            current += 1;
        } else {
            previous = current;
            current = 0;
        }
        best = max(best, previous + current + 1);
    }
    return min(best, 32LL);
}

int main() {
    cout << longestOnesAfterFlip(1775) << endl;
    return 0;
}
