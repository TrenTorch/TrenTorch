#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long mountainPeak(vector<long long> nums) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] < nums[mid + 1]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main() {
    cout << mountainPeak(vector<long long>{1, 3, 5, 4, 2}) << endl;
    return 0;
}
