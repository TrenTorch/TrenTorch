#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long countProductLess(vector<long long> nums, long long k) {
    long long n = nums.size();
    long long product = 1;
    long long left = 0;
    long long total = 0;
    for (long long right = 0; right < n; right++) {
        product *= nums[right];
        while (left <= right && product >= k) {
            product /= nums[left];
            left++;
        }
        total += right - left + 1;
    }
    return total;
}

int main() {
    cout << countProductLess(vector<long long>{10, 5, 2, 6}, 100) << endl;
    return 0;
}
