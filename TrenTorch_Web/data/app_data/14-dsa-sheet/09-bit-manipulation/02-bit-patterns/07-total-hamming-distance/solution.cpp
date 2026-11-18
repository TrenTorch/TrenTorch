#include <bits/stdc++.h>
using namespace std;

// O(30 * n) time, O(1) space
long long totalHammingDistance(vector<long long> nums) {
    long long n = (long long)nums.size();
    long long total = 0;
    for (int i = 0; i < 30; i++) {
        long long ones = 0;
        for (long long x : nums) ones += (x >> i) & 1;
        total += ones * (n - ones);
    }
    return total;
}

int main() {
    cout << totalHammingDistance(vector<long long>{4, 14, 2}) << endl;
    return 0;
}
