#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long upperBound(vector<long long> nums, long long target) {
    long long lo = 0, hi = (long long)nums.size();
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main() {
    cout << upperBound(vector<long long>{1, 2, 2, 2, 5}, 2) << endl;
    return 0;
}
