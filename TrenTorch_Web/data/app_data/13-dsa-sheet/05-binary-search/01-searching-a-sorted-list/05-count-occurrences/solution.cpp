#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long countOccurrences(vector<long long> nums, long long target) {
    long long left = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
    long long right = upper_bound(nums.begin(), nums.end(), target) - nums.begin();
    return right - left;
}

int main() {
    cout << countOccurrences(vector<long long>{1, 2, 2, 2, 3}, 2) << endl;
    return 0;
}
