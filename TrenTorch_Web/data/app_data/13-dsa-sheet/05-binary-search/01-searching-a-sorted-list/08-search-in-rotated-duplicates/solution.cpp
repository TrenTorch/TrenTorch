#include <bits/stdc++.h>
using namespace std;

// O(log n) average time, O(n) worst case (all values equal), O(1) space
bool searchRotatedDuplicates(vector<long long> nums, long long target) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] == target) return true;
        if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) {
            lo += 1;
            hi -= 1;
        } else if (nums[lo] <= nums[mid]) {
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
    return false;
}

int main() {
    cout << boolalpha << searchRotatedDuplicates(vector<long long>{2, 5, 6, 0, 0, 1, 2}, 0) << endl;
    return 0;
}
