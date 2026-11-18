#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long kthMissingPositive(vector<long long> nums, long long k) {
    long long lo = 0, hi = (long long)nums.size();
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] - (mid + 1) < k) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo + k;
}

int main() {
    cout << kthMissingPositive(vector<long long>{2, 3, 4, 7, 11}, 5) << endl;
    return 0;
}
