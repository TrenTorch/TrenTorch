#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long pivotIndex(vector<long long> nums) {
    long long total = 0;
    for (long long x : nums) total += x;
    long long left = 0;
    for (long long i = 0; i < (long long)nums.size(); i++) {
        long long x = nums[i];
        if (left == total - left - x) return i;
        left += x;
    }
    return -1;
}

int main() {
    cout << pivotIndex(vector<long long>{1, 7, 3, 6, 5, 6}) << endl;
    return 0;
}
