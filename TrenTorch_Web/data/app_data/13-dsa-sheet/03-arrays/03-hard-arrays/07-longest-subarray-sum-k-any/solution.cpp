#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
long long longestSubarraySumKAny(vector<long long> nums, long long k) {
    unordered_map<long long, long long> first;
    first.reserve(nums.size() * 2 + 2);
    first[0] = -1;
    long long prefix = 0, best = 0;
    for (long long i = 0; i < (long long)nums.size(); i++) {
        prefix += nums[i];
        auto it = first.find(prefix - k);
        if (it != first.end()) best = max(best, i - it->second);
        first.emplace(prefix, i);
    }
    return best;
}

int main() {
    cout << longestSubarraySumKAny(vector<long long>{1, -1, 5, -2, 3}, 3) << endl;
    return 0;
}
