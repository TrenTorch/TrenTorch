#include <bits/stdc++.h>
using namespace std;

// O(k) time where k is the number of set bits, O(1) space
long long countSetBits(long long n) {
    long long count = 0;
    while (n) {
        n &= n - 1;
        count++;
    }
    return count;
}

int main() {
    cout << countSetBits(13) << endl;
    return 0;
}
