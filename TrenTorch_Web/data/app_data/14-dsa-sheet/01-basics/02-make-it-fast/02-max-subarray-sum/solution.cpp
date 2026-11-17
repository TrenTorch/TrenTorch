#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space (Kadane's algorithm)
long long maxSubarraySum(vector<long long> nums) {
    if (nums.empty()) return 0;
    long long best = nums[0];
    long long cur = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}

int main() {
    cout << maxSubarraySum(vector<long long>{-2, 1, -3, 4, -1, 2, 1, -5, 4}) << endl;
    return 0;
}
