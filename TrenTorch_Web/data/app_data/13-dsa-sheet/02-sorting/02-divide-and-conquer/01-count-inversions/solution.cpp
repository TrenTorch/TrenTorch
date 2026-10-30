#include <bits/stdc++.h>
using namespace std;

// Sorts a[lo, hi) in place (using tmp as scratch) and returns the inversions inside that range.
long long mergeCountInversions(vector<long long>& a, vector<long long>& tmp, size_t lo, size_t hi) {
    if (hi - lo <= 1) return 0;
    size_t mid = lo + (hi - lo) / 2;
    long long total = mergeCountInversions(a, tmp, lo, mid) + mergeCountInversions(a, tmp, mid, hi);
    size_t i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        } else {
            tmp[k++] = a[j++];
            total += (long long)(mid - i);
        }
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    for (size_t t = lo; t < hi; t++) a[t] = tmp[t];
    return total;
}

// O(n log n) time, O(n) space (merge sort that counts cross inversions)
long long countInversions(vector<long long> nums) {
    vector<long long> tmp(nums.size(), 0);
    return mergeCountInversions(nums, tmp, 0, nums.size());
}

int main() {
    cout << countInversions(vector<long long>{3, 1, 2}) << endl;
    return 0;
}
