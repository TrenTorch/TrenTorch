#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long lowestSetBit(long long n) {
    return n & -n;
}

int main() {
    cout << lowestSetBit(12) << endl;
    return 0;
}
