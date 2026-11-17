#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space (sorting copy)
long long threeSumClosest(vector<long long> nums, long long target) {
    vector<long long> a = nums;
    sort(a.begin(), a.end());
    long long n = a.size();
    long long best = a[0] + a[1] + a[2];
    for (long long i = 0; i < n - 2; i++) {
        long long lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long s = a[i] + a[lo] + a[hi];
            long long diff = llabs(s - target);
            long long best_diff = llabs(best - target);
            if (diff < best_diff || (diff == best_diff && s < best)) {
                best = s;
            }
            if (s < target) {
                lo++;
            } else if (s > target) {
                hi--;
            } else {
                return s;
            }
        }
    }
    return best;
}

int main() {
    cout << threeSumClosest(vector<long long>{-1, 2, 1, -4}, 1) << endl;
    return 0;
}
