#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void allSubsetsGo(const vector<long long>& a, long long start, vector<long long>& current,
                  vector<vector<long long>>& out) {
    out.push_back(current);
    for (long long j = start; j < (long long)a.size(); j++) {
        current.push_back(a[j]);
        allSubsetsGo(a, j + 1, current, out);
        current.pop_back();
    }
}

// O(n * 2^n) time, O(n * 2^n) space for the output
vector<vector<long long>> allSubsets(vector<long long> nums) {
    sort(nums.begin(), nums.end());
    vector<vector<long long>> out;
    vector<long long> current;
    allSubsetsGo(nums, 0, current, out);
    return out;
}

int main() {
    cout << allSubsets(vector<long long>{1, 2, 3}) << endl;
    return 0;
}
