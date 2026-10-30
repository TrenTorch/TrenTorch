#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
long long longestZeroSumSubarray(vector<long long> nums) {
    unordered_map<long long, long long> first;
    first.reserve(nums.size() * 2 + 2);
    first[0] = -1;
    long long prefix = 0, best = 0;
    for (long long i = 0; i < (long long)nums.size(); i++) {
        prefix += nums[i];
        auto it = first.find(prefix);
        if (it != first.end()) {
            best = max(best, i - it->second);
        } else {
            first.emplace(prefix, i);
        }
    }
    return best;
}

int main() {
    cout << longestZeroSumSubarray(vector<long long>{15, -2, 2, -8, 1, 7, 10, 23}) << endl;
    return 0;
}
