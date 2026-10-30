#include <bits/stdc++.h>
using namespace std;

// O(n log n + n log D) time, O(1) extra space (D = max position - min position)
long long aggressiveCows(vector<long long> stalls, long long cows) {
    sort(stalls.begin(), stalls.end());

    auto canPlace = [&](long long distance) {
        long long placed = 1, last = stalls[0];
        for (size_t i = 1; i < stalls.size(); i++) {
            if (stalls[i] - last >= distance) {
                placed++;
                last = stalls[i];
            }
        }
        return placed >= cows;
    };

    long long lo = 1, hi = stalls.back() - stalls.front();
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (canPlace(mid)) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return lo;
}

int main() {
    cout << aggressiveCows(vector<long long>{1, 2, 4, 8, 9}, 3) << endl;
    return 0;
}
