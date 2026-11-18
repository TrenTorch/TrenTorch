#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
bool isPowerOfTwo(long long n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int main() {
    cout << boolalpha << isPowerOfTwo(16) << endl;
    return 0;
}
