#include <bits/stdc++.h>
using namespace std;

// Returns {merged, comparisons}.
// O(n + m) time, O(n + m) space
pair<vector<long long>, long long> mergeSortedPair(vector<long long> a, vector<long long> b) {
    vector<long long> merged;
    merged.reserve(a.size() + b.size());
    size_t i = 0, j = 0;
    long long comparisons = 0;
    while (i < a.size() && j < b.size()) {
        comparisons++;
        if (a[i] <= b[j]) {
            merged.push_back(a[i++]);
        } else {
            merged.push_back(b[j++]);
        }
    }
    while (i < a.size()) merged.push_back(a[i++]);
    while (j < b.size()) merged.push_back(b[j++]);
    return {merged, comparisons};
}

int main() {
    return 0;
}
