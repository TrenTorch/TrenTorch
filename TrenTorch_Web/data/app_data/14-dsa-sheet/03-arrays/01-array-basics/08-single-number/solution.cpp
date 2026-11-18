#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long singleNumber(vector<long long> nums) {
    long long result = 0;
    for (long long x : nums) result ^= x;
    return result;
}

int main() {
    cout << singleNumber(vector<long long>{4, 1, 2, 1, 2}) << endl;
    return 0;
}
