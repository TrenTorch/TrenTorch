#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long rotatedMinimum(vector<long long> nums) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] > nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return nums[lo];
}

int main() {
    cout << rotatedMinimum(vector<long long>{4, 5, 6, 7, 0, 1, 2}) << endl;
    return 0;
}
