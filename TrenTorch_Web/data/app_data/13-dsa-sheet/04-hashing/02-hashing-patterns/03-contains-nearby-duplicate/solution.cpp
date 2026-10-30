#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(min(n, k + 1)) space (sliding window of the last k values)
bool containsNearbyDuplicate(vector<long long> nums, long long k) {
    unordered_set<long long> window;
    window.reserve(nums.size() * 2 + 1);
    for (long long i = 0; i < (long long)nums.size(); i++) {
        if (window.count(nums[i])) return true;
        window.insert(nums[i]);
        if (i >= k) window.erase(nums[i - k]);
    }
    return false;
}

int main() {
    cout << boolalpha << containsNearbyDuplicate(vector<long long>{1, 2, 3, 1}, 3) << endl;
    return 0;
}
