#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long longestWithinLimit(vector<long long> nums, long long limit) {
    int n = nums.size();
    deque<int> big, small;
    int left = 0;
    long long best = 0;
    for (int right = 0; right < n; right++) {
        long long x = nums[right];
        while (!big.empty() && nums[big.back()] <= x) big.pop_back();
        big.push_back(right);
        while (!small.empty() && nums[small.back()] >= x) small.pop_back();
        small.push_back(right);
        while (nums[big.front()] - nums[small.front()] > limit) {
            left++;
            if (big.front() < left) big.pop_front();
            if (small.front() < left) small.pop_front();
        }
        best = max(best, (long long)(right - left + 1));
    }
    return best;
}

int main() {
    cout << longestWithinLimit(vector<long long>{8, 2, 4, 7}, 4) << endl;
    return 0;
}
