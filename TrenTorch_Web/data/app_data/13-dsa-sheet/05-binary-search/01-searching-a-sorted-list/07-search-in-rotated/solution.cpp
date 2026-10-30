#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long searchRotated(vector<long long> nums, long long target) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] == target) return mid;
        if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            if (nums[mid] < target && target <= nums[hi]) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    return -1;
}

int main() {
    cout << searchRotated(vector<long long>{4, 5, 6, 7, 0, 1, 2}, 0) << endl;
    return 0;
}
