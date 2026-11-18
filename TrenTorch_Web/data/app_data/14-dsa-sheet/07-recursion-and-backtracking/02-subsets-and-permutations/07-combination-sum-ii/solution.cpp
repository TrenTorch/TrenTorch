#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void combinationSumIiGo(const vector<long long>& a, long long start, long long remaining,
                        vector<long long>& current, vector<vector<long long>>& out) {
    if (remaining == 0) {
        out.push_back(current);
        return;
    }
    for (long long j = start; j < (long long)a.size(); j++) {
        if (j > start && a[j] == a[j - 1]) continue;
        if (a[j] > remaining) break;
        current.push_back(a[j]);
        combinationSumIiGo(a, j + 1, remaining - a[j], current, out);
        current.pop_back();
    }
}

// O(2^n * n) time worst case, O(n) recursion space plus the output
vector<vector<long long>> combinationSumIi(vector<long long> candidates, long long target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<long long>> out;
    vector<long long> current;
    combinationSumIiGo(candidates, 0, target, current, out);
    return out;
}

int main() {
    cout << combinationSumIi(vector<long long>{10, 1, 2, 7, 6, 1, 5}, 8) << endl;
    return 0;
}
