#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space for the result
vector<long long> moveZeros(vector<long long> nums) {
    vector<long long> out;
    out.reserve(nums.size());
    long long zeros = 0;
    for (long long x : nums) {
        if (x != 0) {
            out.push_back(x);
        } else {
            zeros++;
        }
    }
    for (long long z = 0; z < zeros; z++) out.push_back(0);
    return out;
}

int main() {
    cout << moveZeros(vector<long long>{0, 1, 0, 3, 12}) << endl;
    return 0;
}
