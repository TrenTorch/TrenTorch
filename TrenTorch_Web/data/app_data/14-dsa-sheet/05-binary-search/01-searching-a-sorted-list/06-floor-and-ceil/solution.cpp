#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log n) time, O(1) space
vector<long long> floorAndCeil(vector<long long> nums, long long target) {
    long long n = (long long)nums.size();
    long long lo = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
    long long ceilVal = lo < n ? nums[lo] : -1;
    long long floorVal;
    if (lo < n && nums[lo] == target) {
        floorVal = target;
    } else {
        floorVal = lo > 0 ? nums[lo - 1] : -1;
    }
    return {floorVal, ceilVal};
}

int main() {
    cout << floorAndCeil(vector<long long>{1, 2, 8, 10, 11, 12, 19}, 5) << endl;
    return 0;
}
