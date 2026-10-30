#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long longestSubarraySumK(vector<long long> nums, long long k) {
    long long best = 0, left = 0, total = 0;
    long long n = nums.size();
    for (long long right = 0; right < n; right++) {
        total += nums[right];
        while (total > k && left <= right) {
            total -= nums[left];
            left++;
        }
        if (total == k) best = max(best, right - left + 1);
    }
    return best;
}

int main() {
    cout << longestSubarraySumK(vector<long long>{1, 2, 3, 1, 1, 1, 1}, 3) << endl;
    return 0;
}
