#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long longestOnes(vector<long long> nums, long long k) {
    long long n = nums.size();
    long long zeros = 0;
    long long left = 0;
    long long best = 0;
    for (long long right = 0; right < n; right++) {
        if (nums[right] == 0) {
            zeros++;
        }
        while (zeros > k) {
            if (nums[left] == 0) {
                zeros--;
            }
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best;
}

int main() {
    cout << longestOnes(vector<long long>{1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0}, 2) << endl;
    return 0;
}
