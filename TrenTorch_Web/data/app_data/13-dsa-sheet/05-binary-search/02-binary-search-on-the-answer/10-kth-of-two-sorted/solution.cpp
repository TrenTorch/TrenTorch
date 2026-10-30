#include <bits/stdc++.h>
using namespace std;

// O(log(min(m, n))) time, O(1) space
long long kthOfTwoSorted(vector<long long> a, vector<long long> b, long long k) {
    if (a.size() > b.size()) {
        swap(a, b);
    }
    long long m = (long long)a.size(), n = (long long)b.size();
    const long long NEG = LLONG_MIN, POS = LLONG_MAX;
    long long lo = max(0LL, k - n), hi = min(k, m);
    while (lo <= hi) {
        long long i = (lo + hi) / 2;
        long long j = k - i;
        long long aLeft = i > 0 ? a[i - 1] : NEG;
        long long aRight = i < m ? a[i] : POS;
        long long bLeft = j > 0 ? b[j - 1] : NEG;
        long long bRight = j < n ? b[j] : POS;
        if (aLeft <= bRight && bLeft <= aRight) {
            return max(aLeft, bLeft);
        }
        if (aLeft > bRight) {
            hi = i - 1;
        } else {
            lo = i + 1;
        }
    }
    return 0;
}

int main() {
    cout << kthOfTwoSorted(vector<long long>{2, 3, 6, 7, 9}, vector<long long>{1, 4, 8, 10}, 5) << endl;
    return 0;
}
