#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
long long countPairsWithSum(vector<long long> nums, long long target) {
    unordered_map<long long, long long> seen;
    seen.reserve(nums.size() * 2 + 1);
    long long count = 0;
    for (long long x : nums) {
        auto it = seen.find(target - x);
        if (it != seen.end()) count += it->second;
        seen[x]++;
    }
    return count;
}

int main() {
    cout << countPairsWithSum(vector<long long>{1, 2, 3, 4, 3}, 6) << endl;
    return 0;
}
