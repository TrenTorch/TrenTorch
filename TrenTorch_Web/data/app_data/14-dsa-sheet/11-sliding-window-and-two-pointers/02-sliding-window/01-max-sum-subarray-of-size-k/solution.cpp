#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxSumK(vector<long long> nums, long long k) {
    long long n = nums.size();
    long long total = 0;
    for (long long i = 0; i < k; i++) {
        total += nums[i];
    }
    long long best = total;
    for (long long i = k; i < n; i++) {
        total += nums[i] - nums[i - k];
        best = max(best, total);
    }
    return best;
}

int main() {
    cout << maxSumK(vector<long long>{2, 1, 5, 1, 3, 2}, 3) << endl;
    return 0;
}
