#include <bits/stdc++.h>
using namespace std;

// Counts subarrays with at most m odd numbers. O(n) time, O(1) space.
static long long atMostOdd(const vector<long long>& nums, long long m) {
    if (m < 0) {
        return 0;
    }
    long long n = nums.size();
    long long odd = 0;
    long long left = 0;
    long long total = 0;
    for (long long right = 0; right < n; right++) {
        odd += nums[right] % 2;
        while (odd > m) {
            odd -= nums[left] % 2;
            left++;
        }
        total += right - left + 1;
    }
    return total;
}

// O(n) time, O(1) space (two sliding-window passes)
long long numberOfSubarrays(vector<long long> nums, long long k) {
    return atMostOdd(nums, k) - atMostOdd(nums, k - 1);
}

int main() {
    cout << numberOfSubarrays(vector<long long>{1, 1, 2, 1, 1}, 3) << endl;
    return 0;
}
