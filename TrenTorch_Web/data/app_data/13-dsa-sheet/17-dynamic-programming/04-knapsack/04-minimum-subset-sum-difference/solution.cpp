#include <bits/stdc++.h>
using namespace std;

// O(len(nums) * total) time, O(total) space
long long minSubsetDifference(vector<long long> nums) {
    long long total = 0;
    for (long long x : nums) total += x;
    vector<char> reach(total + 1, 0);
    reach[0] = 1;
    for (long long x : nums) {
        for (long long s = total; s >= x; --s) {
            if (reach[s - x]) reach[s] = 1;
        }
    }
    for (long long s = total / 2; s >= 0; --s) {
        if (reach[s]) return total - 2 * s;
    }
    return total;
}

int main() {
    cout << minSubsetDifference(vector<long long>{1, 6, 11, 5}) << endl;
    return 0;
}
