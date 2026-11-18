#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n * 2^n) time, O(2^n) space
vector<long long> allSubsetSums(vector<long long> nums) {
    vector<long long> sums = {0};
    for (long long x : nums) {
        // sums is sorted, so the shifted copy is sorted too; merge the two in linear time
        vector<long long> shifted;
        shifted.reserve(sums.size());
        for (long long s : sums) shifted.push_back(s + x);
        vector<long long> merged(sums.size() + shifted.size());
        merge(sums.begin(), sums.end(), shifted.begin(), shifted.end(), merged.begin());
        sums = std::move(merged);
    }
    return sums;
}

int main() {
    cout << allSubsetSums(vector<long long>{1, 2}) << endl;
    return 0;
}
