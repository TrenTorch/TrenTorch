#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
bool isPowerOfFour(long long n) {
    return n > 0 && (n & (n - 1)) == 0 && (n & 0x5555555555555555LL) != 0;
}

int main() {
    cout << boolalpha << isPowerOfFour(16) << endl;
    return 0;
}
