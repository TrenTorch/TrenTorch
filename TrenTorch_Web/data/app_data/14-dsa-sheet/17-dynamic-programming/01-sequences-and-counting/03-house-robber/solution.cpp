#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long rob(vector<long long> nums) {
    long long skip = 0, take = 0;
    for (long long x : nums) {
        long long nextSkip = max(skip, take);
        take = skip + x;
        skip = nextSkip;
    }
    return max(skip, take);
}

int main() {
    cout << rob(vector<long long>{1, 2, 3, 1}) << endl;
    return 0;
}
