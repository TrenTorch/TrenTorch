#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space (sorted copy of intervals)
long long eraseOverlap(vector<vector<long long>> intervals) {
    stable_sort(intervals.begin(), intervals.end(), [](const vector<long long>& a, const vector<long long>& b) {
        return a[1] < b[1];
    });
    long long removed = 0;
    bool hasLast = false;
    long long lastEnd = 0;
    for (const auto& iv : intervals) {
        long long start = iv[0];
        long long end = iv[1];
        if (!hasLast || start >= lastEnd) {
            hasLast = true;
            lastEnd = end;
        } else {
            removed++;
        }
    }
    return removed;
}

int main() {
    cout << eraseOverlap(vector<vector<long long>>{vector<long long>{1, 2}, vector<long long>{2, 3}, vector<long long>{3, 4}, vector<long long>{1, 3}}) << endl;
    return 0;
}
