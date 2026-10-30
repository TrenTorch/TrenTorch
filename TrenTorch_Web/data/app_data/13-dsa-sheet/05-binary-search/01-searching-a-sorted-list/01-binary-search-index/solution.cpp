#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long binarySearchIndex(vector<long long> nums, long long target) {
    long long lo = 0, hi = (long long)nums.size() - 1;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

int main() {
    cout << binarySearchIndex(vector<long long>{-1, 0, 3, 5, 9, 12}, 9) << endl;
    return 0;
}
