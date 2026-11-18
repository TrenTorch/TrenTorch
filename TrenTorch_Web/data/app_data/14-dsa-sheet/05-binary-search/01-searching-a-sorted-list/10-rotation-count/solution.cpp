#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long rotationCount(vector<long long> nums) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] > nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main() {
    cout << rotationCount(vector<long long>{3, 4, 5, 1, 2}) << endl;
    return 0;
}
