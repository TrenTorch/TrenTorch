#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log n) time, O(1) space
vector<long long> firstAndLast(vector<long long> nums, long long target) {
    long long n = (long long)nums.size();
    long long first = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
    if (first == n || nums[first] != target) return {-1, -1};
    long long last = upper_bound(nums.begin(), nums.end(), target) - nums.begin() - 1;
    return {first, last};
}

int main() {
    cout << firstAndLast(vector<long long>{5, 7, 7, 8, 8, 10}, 8) << endl;
    return 0;
}
