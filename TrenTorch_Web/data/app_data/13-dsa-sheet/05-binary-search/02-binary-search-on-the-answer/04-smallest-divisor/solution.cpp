#include <bits/stdc++.h>
using namespace std;

// O(n log(max value)) time, O(1) space
long long smallestDivisor(vector<long long> nums, long long threshold) {
    long long lo = 1, hi = *max_element(nums.begin(), nums.end());
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        long long total = 0;
        for (long long x : nums) {
            total += (x + mid - 1) / mid;
        }
        if (total <= threshold) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    cout << smallestDivisor(vector<long long>{1, 2, 5, 9}, 6) << endl;
    return 0;
}
