#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long countSubarraysSumK(vector<long long> nums, long long k) {
    unordered_map<long long, long long> seen;
    seen[0] = 1;
    long long prefix = 0, result = 0;
    for (long long x : nums) {
        prefix += x;
        auto it = seen.find(prefix - k);
        if (it != seen.end()) result += it->second;
        seen[prefix]++;
    }
    return result;
}

int main() {
    cout << countSubarraysSumK(vector<long long>{1, 1, 1}, 2) << endl;
    return 0;
}
