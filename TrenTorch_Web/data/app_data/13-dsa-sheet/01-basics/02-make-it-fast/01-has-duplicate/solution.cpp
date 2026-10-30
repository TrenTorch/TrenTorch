#include <bits/stdc++.h>
using namespace std;

// O(n) expected time, O(n) space
bool hasDuplicate(vector<long long> nums) {
    unordered_set<long long> seen;
    seen.reserve(nums.size() * 2 + 1);
    for (long long x : nums) {
        if (!seen.insert(x).second) return true;
    }
    return false;
}

int main() {
    cout << boolalpha << hasDuplicate(vector<long long>{1, 2, 3, 1}) << endl;
    return 0;
}
