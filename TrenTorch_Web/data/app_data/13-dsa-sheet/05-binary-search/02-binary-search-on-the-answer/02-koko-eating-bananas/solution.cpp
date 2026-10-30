#include <bits/stdc++.h>
using namespace std;

// O(p log(max pile)) time, where p = number of piles; O(1) space
long long minEatingSpeed(vector<long long> piles, long long hours) {
    long long lo = 1, hi = *max_element(piles.begin(), piles.end());
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        long long needed = 0;
        for (long long p : piles) {
            needed += (p + mid - 1) / mid;
        }
        if (needed <= hours) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    cout << minEatingSpeed(vector<long long>{3, 6, 7, 11}, 8) << endl;
    return 0;
}
