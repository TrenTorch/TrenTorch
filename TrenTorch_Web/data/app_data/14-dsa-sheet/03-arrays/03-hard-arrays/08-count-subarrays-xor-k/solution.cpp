#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
long long countSubarraysXorK(vector<long long> nums, long long k) {
    unordered_map<long long, long long> seen;
    seen.reserve(nums.size() * 2 + 2);
    seen[0] = 1;
    long long prefix = 0, count = 0;
    for (long long x : nums) {
        prefix ^= x;
        auto it = seen.find(prefix ^ k);
        if (it != seen.end()) count += it->second;
        seen[prefix] += 1;
    }
    return count;
}

int main() {
    cout << countSubarraysXorK(vector<long long>{4, 2, 2, 6, 4}, 6) << endl;
    return 0;
}
