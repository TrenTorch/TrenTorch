#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void subsetsWithDuplicatesGo(const vector<long long>& a, long long start, vector<long long>& current,
                             vector<vector<long long>>& out) {
    out.push_back(current);
    for (long long j = start; j < (long long)a.size(); j++) {
        if (j > start && a[j] == a[j - 1]) continue;
        current.push_back(a[j]);
        subsetsWithDuplicatesGo(a, j + 1, current, out);
        current.pop_back();
    }
}

// O(n * 2^n) time, O(n * 2^n) space for the output
vector<vector<long long>> subsetsWithDuplicates(vector<long long> nums) {
    sort(nums.begin(), nums.end());
    vector<vector<long long>> out;
    vector<long long> current;
    subsetsWithDuplicatesGo(nums, 0, current, out);
    return out;
}

int main() {
    cout << subsetsWithDuplicates(vector<long long>{1, 2, 2}) << endl;
    return 0;
}
