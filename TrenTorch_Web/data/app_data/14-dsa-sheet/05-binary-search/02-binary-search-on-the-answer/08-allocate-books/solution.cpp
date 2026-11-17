#include <bits/stdc++.h>
using namespace std;

// O(n log S) time, where S = sum of pages; O(1) extra space
long long allocateBooks(vector<long long> pages, long long students) {
    if (students > (long long)pages.size()) {
        return -1;
    }
    long long lo = *max_element(pages.begin(), pages.end());
    long long hi = accumulate(pages.begin(), pages.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        long long needed = 1, load = 0;
        for (long long p : pages) {
            if (load + p > mid) {
                needed++;
                load = 0;
            }
            load += p;
        }
        if (needed <= students) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    cout << allocateBooks(vector<long long>{12, 34, 67, 90}, 2) << endl;
    return 0;
}
