#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time, O(n) space (sorts a copy)
vector<long long> kSmallest(vector<long long> nums, long long k) {
    if (k <= 0) return {};
    sort(nums.begin(), nums.end());
    if ((long long)nums.size() > k) nums.resize((size_t)k);
    return nums;
}

int main() {
    cout << kSmallest(vector<long long>{7, 2, 9, 4, 2}, 3) << endl;
    return 0;
}
