#include <bits/stdc++.h>
using namespace std;

// O(n^2) time, O(n) space (sorting copy)
long long countTripletsSmaller(vector<long long> nums, long long target) {
    vector<long long> a = nums;
    sort(a.begin(), a.end());
    long long n = a.size();
    long long count = 0;
    for (long long i = 0; i < n - 2; i++) {
        long long lo = i + 1, hi = n - 1;
        while (lo < hi) {
            if (a[i] + a[lo] + a[hi] < target) {
                count += hi - lo;
                lo++;
            } else {
                hi--;
            }
        }
    }
    return count;
}

int main() {
    cout << countTripletsSmaller(vector<long long>{-2, 0, 1, 3}, 2) << endl;
    return 0;
}
