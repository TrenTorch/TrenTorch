#include <bits/stdc++.h>
using namespace std;

// O(n log(sum of weights)) time, O(1) space
long long shipCapacity(vector<long long> weights, long long days) {
    long long lo = *max_element(weights.begin(), weights.end());
    long long hi = accumulate(weights.begin(), weights.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        long long needed = 1, load = 0;
        for (long long w : weights) {
            if (load + w > mid) {
                needed += 1;
                load = 0;
            }
            load += w;
        }
        if (needed <= days) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    cout << shipCapacity(vector<long long>{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, 5) << endl;
    return 0;
}
