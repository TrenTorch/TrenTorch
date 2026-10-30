#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n^2) time, O(n) space (sorted copy; the output is not counted)
vector<vector<long long>> threeSum(vector<long long> nums) {
    vector<long long> a = nums;
    sort(a.begin(), a.end());
    int n = a.size();
    vector<vector<long long>> out;
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long total = a[i] + a[lo] + a[hi];
            if (total < 0) {
                lo++;
            } else if (total > 0) {
                hi--;
            } else {
                out.push_back({a[i], a[lo], a[hi]});
                lo++;
                hi--;
                while (lo < hi && a[lo] == a[lo - 1]) lo++;
                while (lo < hi && a[hi] == a[hi + 1]) hi--;
            }
        }
    }
    return out;
}

int main() {
    cout << threeSum(vector<long long>{-1, 0, 1, 2, -1, -4}) << endl;
    return 0;
}
