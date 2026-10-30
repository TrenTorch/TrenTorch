#include <bits/stdc++.h>
using namespace std;

// O(log(min(m, n))) time, O(1) space
double medianTwoSorted(vector<long long> a, vector<long long> b) {
    if (a.size() > b.size()) {
        swap(a, b);
    }
    long long m = (long long)a.size(), n = (long long)b.size();
    long long half = (m + n + 1) / 2;
    const long long NEG = LLONG_MIN, POS = LLONG_MAX;
    long long lo = 0, hi = m;
    while (lo <= hi) {
        long long i = (lo + hi) / 2;
        long long j = half - i;
        long long aLeft = i > 0 ? a[i - 1] : NEG;
        long long aRight = i < m ? a[i] : POS;
        long long bLeft = j > 0 ? b[j - 1] : NEG;
        long long bRight = j < n ? b[j] : POS;
        if (aLeft <= bRight && bLeft <= aRight) {
            if ((m + n) % 2 == 1) {
                return (double)max(aLeft, bLeft);
            }
            return (double)(max(aLeft, bLeft) + min(aRight, bRight)) / 2.0;
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
    cout << medianTwoSorted(vector<long long>{1, 3}, vector<long long>{2}) << endl;
    return 0;
}
