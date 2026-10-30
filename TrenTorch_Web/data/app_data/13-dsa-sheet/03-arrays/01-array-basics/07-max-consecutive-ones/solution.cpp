#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long maxConsecutiveOnes(vector<long long> nums) {
    long long best = 0, current = 0;
    for (long long x : nums) {
        if (x == 1) {
            current++;
            best = max(best, current);
        } else {
            current = 0;
        }
    }
    return best;
}

int main() {
    cout << maxConsecutiveOnes(vector<long long>{1, 1, 0, 1, 1, 1}) << endl;
    return 0;
}
