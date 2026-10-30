#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long swapOddEvenBits(long long n) {
    return ((n & 0x55555555LL) << 1) | ((n & 0xAAAAAAAALL) >> 1);
}

int main() {
    cout << swapOddEvenBits(10) << endl;
    return 0;
}
