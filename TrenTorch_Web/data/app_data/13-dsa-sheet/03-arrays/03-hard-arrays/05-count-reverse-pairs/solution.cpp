#include <bits/stdc++.h>
using namespace std;

// Sorts a[lo, hi) ascending and returns the number of reverse pairs inside it.
long long reversePairsRec(vector<long long>& a, int lo, int hi) {
    if (hi - lo <= 1) return 0;
    int mid = lo + (hi - lo) / 2;
    long long count = reversePairsRec(a, lo, mid) + reversePairsRec(a, mid, hi);
    int j = mid;
    for (int i = lo; i < mid; i++) {
        while (j < hi && a[i] > 2 * a[j]) j++;
        count += j - mid;
    }
    inplace_merge(a.begin() + lo, a.begin() + mid, a.begin() + hi);
    return count;
}

// O(n log n) time, O(n) space
long long countReversePairs(vector<long long> nums) {
    return reversePairsRec(nums, 0, (int)nums.size());
}

int main() {
    cout << countReversePairs(vector<long long>{1, 3, 2, 3, 1}) << endl;
    return 0;
}
