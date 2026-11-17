#include <bits/stdc++.h>
using namespace std;

// O(n log(max bloom day)) time, O(1) space
long long minDaysBouquets(vector<long long> bloom, long long m, long long k) {
    if (m * k > (long long)bloom.size()) return -1;

    auto possible = [&](long long day) {
        long long bouquets = 0, run = 0;
        for (long long b : bloom) {
            if (b <= day) {
                run += 1;
                if (run == k) {
                    bouquets += 1;
                    run = 0;
                }
            } else {
                run = 0;
            }
        }
        return bouquets >= m;
    };

    long long lo = *min_element(bloom.begin(), bloom.end());
    long long hi = *max_element(bloom.begin(), bloom.end());
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (possible(mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    cout << minDaysBouquets(vector<long long>{1, 10, 3, 10, 2}, 3, 1) << endl;
    return 0;
}
