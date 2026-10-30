#include <bits/stdc++.h>
using namespace std;

// O(1) time (fixed 32 iterations), O(1) space
long long reverseBits(long long n) {
    long long result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}

int main() {
    cout << reverseBits(1) << endl;
    return 0;
}
