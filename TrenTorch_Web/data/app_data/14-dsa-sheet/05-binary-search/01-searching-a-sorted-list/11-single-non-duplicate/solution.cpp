#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long singleNonDuplicate(vector<long long> nums) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (mid % 2 == 1) mid -= 1;
        if (nums[mid] == nums[mid + 1]) {
            lo = mid + 2;
        } else {
            hi = mid;
        }
    }
    return nums[lo];
}

int main() {
    cout << singleNonDuplicate(vector<long long>{1, 1, 2, 3, 3, 4, 4, 8, 8}) << endl;
    return 0;
}
