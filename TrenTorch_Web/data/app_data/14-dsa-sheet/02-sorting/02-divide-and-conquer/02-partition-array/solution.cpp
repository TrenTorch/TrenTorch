#include <bits/stdc++.h>
using namespace std;

// Lomuto partition with the last value as pivot. Returns {rearranged array, final pivot index}.
// O(n) time, O(n) space for the copy
pair<vector<long long>, long long> partitionArray(vector<long long> nums) {
    vector<long long> a = nums;
    long long pivot = a.back();
    long long i = -1;
    for (size_t j = 0; j + 1 < a.size(); j++) {
        if (a[j] <= pivot) {
            i++;
            swap(a[(size_t)i], a[j]);
        }
    }
    swap(a[(size_t)(i + 1)], a[a.size() - 1]);
    return {a, i + 1};
}

int main() {
    return 0;
}
