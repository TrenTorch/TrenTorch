#include <bits/stdc++.h>
using namespace std;

// O(n * S / 64) time with S = sum of nums (sum <= 20000 by constraints), O(S) space
bool canPartition(vector<long long> nums) {
    long long total = 0;
    for (long long x : nums) total += x;
    if (total % 2 != 0) return false;
    bitset<20001> bits;
    bits.set(0);
    for (long long x : nums) {
        bits |= bits << x;
    }
    return bits[total / 2];
}

int main() {
    cout << boolalpha << canPartition(vector<long long>{1, 5, 11, 5}) << endl;
    return 0;
}
