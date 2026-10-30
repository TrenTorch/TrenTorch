#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space for the result
vector<long long> dedupeSorted(vector<long long> nums) {
    vector<long long> out;
    for (long long x : nums) {
        if (out.empty() || out.back() != x) out.push_back(x);
    }
    return out;
}

int main() {
    cout << dedupeSorted(vector<long long>{1, 1, 2, 2, 2, 3}) << endl;
    return 0;
}
