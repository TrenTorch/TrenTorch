#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxProductSubarray(vector<long long> nums) {
    long long best = nums[0], hi = nums[0], lo = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        long long x = nums[i];
        long long c0 = x, c1 = hi * x, c2 = lo * x;
        hi = max({c0, c1, c2});
        lo = min({c0, c1, c2});
        best = max(best, hi);
    }
    return best;
}

int main() {
    cout << maxProductSubarray(vector<long long>{2, 3, -2, 4}) << endl;
    return 0;
}
