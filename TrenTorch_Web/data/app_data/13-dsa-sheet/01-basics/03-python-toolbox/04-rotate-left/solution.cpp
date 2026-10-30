#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space (returns a new vector; the input is not changed)
vector<long long> rotateLeft(vector<long long> nums, long long k) {
    if (nums.empty()) return {};
    size_t shift = (size_t)(k % (long long)nums.size());
    rotate(nums.begin(), nums.begin() + shift, nums.end());
    return nums;
}

int main() {
    cout << rotateLeft(vector<long long>{1, 2, 3, 4, 5}, 2) << endl;
    return 0;
}
