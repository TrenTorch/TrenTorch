#include <bits/stdc++.h>
using namespace std;

// O(n * D) time, D = number of distinct running sums, O(D) space
long long findTargetSumWays(vector<long long> nums, long long target) {
    unordered_map<long long, long long> ways;
    ways[0] = 1;
    for (long long x : nums) {
        unordered_map<long long, long long> nxt;
        for (const auto& [s, count] : ways) {
            nxt[s + x] += count;
            nxt[s - x] += count;
        }
        ways = move(nxt);
    }
    auto it = ways.find(target);
    return it == ways.end() ? 0 : it->second;
}

int main() {
    cout << findTargetSumWays(vector<long long>{1, 1, 1, 1, 1}, 3) << endl;
    return 0;
}
