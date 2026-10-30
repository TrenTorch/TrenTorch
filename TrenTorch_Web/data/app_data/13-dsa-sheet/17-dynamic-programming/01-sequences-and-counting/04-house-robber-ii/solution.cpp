#include <bits/stdc++.h>
using namespace std;

long long lineRob(const vector<long long>& houses, size_t from, size_t to) {
    long long skip = 0, take = 0;
    for (size_t i = from; i < to; i++) {
        long long x = houses[i];
        long long nskip = max(skip, take);
        take = skip + x;
        skip = nskip;
    }
    return max(skip, take);
}

// O(n) time, O(1) extra space
long long robCircle(vector<long long> nums) {
    size_t n = nums.size();
    if (n == 0) return 0;
    if (n == 1) return nums[0];
    return max(lineRob(nums, 1, n), lineRob(nums, 0, n - 1));
}

int main() {
    cout << robCircle(vector<long long>{2, 3, 2}) << endl;
    return 0;
}
