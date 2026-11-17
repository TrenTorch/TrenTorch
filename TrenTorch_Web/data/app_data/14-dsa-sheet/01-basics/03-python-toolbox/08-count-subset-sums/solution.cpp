#include <bits/stdc++.h>
using namespace std;

// (size, sum) -> number of subsets of `values` with that size and sum
map<pair<long long, long long>, long long> sumsBySize(const vector<long long>& values) {
    map<pair<long long, long long>, long long> states;
    states[make_pair(0LL, 0LL)] = 1;
    for (long long v : values) {
        vector<pair<pair<long long, long long>, long long>> snapshot(states.begin(), states.end());
        for (const auto& entry : snapshot) {
            states[make_pair(entry.first.first + 1, entry.first.second + v)] += entry.second;
        }
    }
    return states;
}

// O(2^(n/2) * log(2^(n/2))) time, O(2^(n/2)) space (meet in the middle)
long long countSubsetSums(vector<long long> nums, long long k, long long target) {
    size_t half = nums.size() / 2;
    vector<long long> leftVals(nums.begin(), nums.begin() + half);
    vector<long long> rightVals(nums.begin() + half, nums.end());
    auto left = sumsBySize(leftVals);
    auto right = sumsBySize(rightVals);
    long long count = 0;
    for (const auto& entry : right) {
        auto it = left.find(make_pair(k - entry.first.first, target - entry.first.second));
        if (it != left.end()) count += entry.second * it->second;
    }
    return count;
}

int main() {
    cout << countSubsetSums(vector<long long>{1, 2, 3, 4}, 2, 5) << endl;
    return 0;
}
