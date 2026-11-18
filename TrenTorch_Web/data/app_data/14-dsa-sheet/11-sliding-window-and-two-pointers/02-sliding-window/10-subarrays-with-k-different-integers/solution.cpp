#include <bits/stdc++.h>
using namespace std;

// Counts subarrays with at most m distinct values. O(n log d) time, O(d) space.
static long long atMostDistinct(const vector<long long>& nums, long long m) {
    map<long long, long long> count;
    long long n = nums.size();
    long long left = 0;
    long long total = 0;
    for (long long right = 0; right < n; right++) {
        count[nums[right]]++;
        while ((long long)count.size() > m) {
            long long gone = nums[left];
            count[gone]--;
            if (count[gone] == 0) {
                count.erase(gone);
            }
            left++;
        }
        total += right - left + 1;
    }
    return total;
}

// O(n log n) time, O(n) space (two sliding-window passes)
long long subarraysKDistinct(vector<long long> nums, long long k) {
    return atMostDistinct(nums, k) - atMostDistinct(nums, k - 1);
}

int main() {
    cout << subarraysKDistinct(vector<long long>{1, 2, 1, 2, 3}, 2) << endl;
    return 0;
}
