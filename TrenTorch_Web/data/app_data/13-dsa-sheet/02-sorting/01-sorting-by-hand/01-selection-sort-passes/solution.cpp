#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n^2) time, O(n^2) space for the snapshots
vector<vector<long long>> selectionSortPasses(vector<long long> nums) {
    vector<vector<long long>> passes;
    vector<long long> a = nums;
    size_t n = a.size();
    for (size_t i = 0; i + 1 < n; i++) {
        size_t smallest = i;
        for (size_t j = i + 1; j < n; j++) {
            if (a[j] < a[smallest]) smallest = j;
        }
        swap(a[i], a[smallest]);
        passes.push_back(a);
    }
    return passes;
}

int main() {
    cout << selectionSortPasses(vector<long long>{64, 25, 12, 22, 11}) << endl;
    return 0;
}
