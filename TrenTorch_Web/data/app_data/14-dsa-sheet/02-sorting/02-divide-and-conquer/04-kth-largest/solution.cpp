#include <bits/stdc++.h>
using namespace std;

// Quickselect via nth_element. O(n) average time, O(1) extra space (copy of nums is by value).
long long kthLargest(vector<long long> nums, long long k) {
    size_t idx = nums.size() - (size_t)k;  // ascending index of the k-th largest
    nth_element(nums.begin(), nums.begin() + idx, nums.end());
    return nums[idx];
}

int main() {
    cout << kthLargest(vector<long long>{3, 2, 1, 5, 6, 4}, 2) << endl;
    return 0;
}
