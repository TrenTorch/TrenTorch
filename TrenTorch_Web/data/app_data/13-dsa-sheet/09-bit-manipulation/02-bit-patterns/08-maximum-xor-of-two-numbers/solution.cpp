#include <bits/stdc++.h>
using namespace std;

// O(30 * n) time, O(n) space
long long maxXorPair(vector<long long> nums) {
    long long best = 0;
    for (int bit = 29; bit >= 0; bit--) {
        unordered_set<long long> prefixes;
        for (long long x : nums) prefixes.insert(x >> bit);
        long long candidate = (best << 1) | 1;
        best <<= 1;
        for (long long p : prefixes) {
            if (prefixes.count(p ^ candidate)) {
                best = candidate;
                break;
            }
        }
    }
    return best;
}

int main() {
    cout << maxXorPair(vector<long long>{3, 10, 5, 25, 2, 8}) << endl;
    return 0;
}
