#include <bits/stdc++.h>
using namespace std;

// O(len(nums) * target / 64) time with bitset, O(target) space
bool subsetSum(vector<long long> nums, long long target) {
    const size_t MAXBITS = 100001;
    bitset<MAXBITS> bits;
    bits[0] = 1;
    for (long long x : nums) {
        bits |= bits << (size_t)x;
    }
    return bits[(size_t)target];
}

int main() {
    cout << boolalpha << subsetSum(vector<long long>{3, 34, 4, 12, 5, 2}, 9) << endl;
    return 0;
}
