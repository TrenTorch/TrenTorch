#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long missingNumber(vector<long long> nums) {
    long long n = nums.size();
    long long expected = n * (n + 1) / 2;
    long long actual = 0;
    for (long long x : nums) actual += x;
    return expected - actual;
}

int main() {
    cout << missingNumber(vector<long long>{3, 0, 1}) << endl;
    return 0;
}
