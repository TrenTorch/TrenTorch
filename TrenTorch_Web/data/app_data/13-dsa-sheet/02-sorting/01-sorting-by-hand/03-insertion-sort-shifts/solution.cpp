#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space (Fenwick tree over value ranks)
long long insertionSortShifts(vector<long long> nums) {
    vector<long long> uniq = nums;
    sort(uniq.begin(), uniq.end());
    uniq.erase(unique(uniq.begin(), uniq.end()), uniq.end());
    long long size = (long long)uniq.size();
    vector<long long> tree(size + 1, 0);
    long long shifts = 0;
    for (size_t seen = 0; seen < nums.size(); seen++) {
        long long x = nums[seen];
        long long rank = (long long)(lower_bound(uniq.begin(), uniq.end(), x) - uniq.begin()) + 1;
        long long notBigger = 0;
        for (long long i = rank; i > 0; i -= i & -i) {
            notBigger += tree[i];
        }
        shifts += (long long)seen - notBigger;
        for (long long i = rank; i <= size; i += i & -i) {
            tree[i] += 1;
        }
    }
    return shifts;
}

int main() {
    cout << insertionSortShifts(vector<long long>{3, 1, 2}) << endl;
    return 0;
}
