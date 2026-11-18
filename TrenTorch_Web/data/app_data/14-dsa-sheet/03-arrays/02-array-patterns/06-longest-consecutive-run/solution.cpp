#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long longestConsecutive(vector<long long> nums) {
    unordered_set<long long> values(nums.begin(), nums.end());
    long long best = 0;
    for (long long x : values) {
        if (values.find(x - 1) == values.end()) {
            long long length = 1;
            while (values.find(x + length) != values.end()) length++;
            best = max(best, length);
        }
    }
    return best;
}

int main() {
    cout << longestConsecutive(vector<long long>{100, 4, 200, 1, 3, 2}) << endl;
    return 0;
}
