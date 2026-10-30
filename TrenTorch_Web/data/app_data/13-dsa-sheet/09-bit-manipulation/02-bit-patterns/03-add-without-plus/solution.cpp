#include <bits/stdc++.h>
using namespace std;

// O(1) time (at most 32 carry rounds), O(1) space
long long bitAdd(long long a, long long b) {
    const unsigned long long mask = 0xFFFFFFFFULL;
    unsigned long long ua = (unsigned long long)a & mask;
    unsigned long long ub = (unsigned long long)b & mask;
    while (ub) {
        unsigned long long carry = ((ua & ub) << 1) & mask;
        ua = (ua ^ ub) & mask;
        ub = carry;
    }
    if (ua >= (1ULL << 31)) return (long long)ua - (1LL << 32);
    return (long long)ua;
}

int main() {
    cout << bitAdd(1, 2) << endl;
    return 0;
}
