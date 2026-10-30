#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(min(n, k)) space
long long subarraysDivisibleByK(vector<long long> nums, long long k) {
    unordered_map<long long, long long> seen;
    seen.reserve(nums.size() * 2 + 2);
    seen[0] = 1;
    long long prefix = 0, count = 0;
    for (long long x : nums) {
        prefix = ((prefix + x) % k + k) % k;  // non-negative remainder, like Python's %
        auto it = seen.find(prefix);
        if (it != seen.end()) count += it->second;
        seen[prefix] += 1;
    }
    return count;
}

int main() {
    cout << subarraysDivisibleByK(vector<long long>{4, 5, 0, -2, -3, 1}, 5) << endl;
    return 0;
}
