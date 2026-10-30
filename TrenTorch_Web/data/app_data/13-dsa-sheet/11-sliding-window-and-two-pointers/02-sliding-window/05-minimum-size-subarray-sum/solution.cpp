#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long minSubarrayLen(long long target, vector<long long> nums) {
    long long n = nums.size();
    long long best = n + 1;
    long long total = 0;
    long long left = 0;
    for (long long right = 0; right < n; right++) {
        total += nums[right];
        while (total >= target) {
            best = min(best, right - left + 1);
            total -= nums[left];
            left++;
        }
    }
    return best <= n ? best : 0;
}

int main() {
    cout << minSubarrayLen(7, vector<long long>{2, 3, 1, 2, 4, 3}) << endl;
    return 0;
}
