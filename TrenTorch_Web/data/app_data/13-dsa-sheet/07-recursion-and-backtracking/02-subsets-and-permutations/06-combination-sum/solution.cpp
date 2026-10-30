#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void combinationSumGo(const vector<long long>& a, long long start, long long remaining,
                      vector<long long>& current, vector<vector<long long>>& out) {
    if (remaining == 0) {
        out.push_back(current);
        return;
    }
    for (long long j = start; j < (long long)a.size(); j++) {
        if (a[j] > remaining) break;
        current.push_back(a[j]);
        combinationSumGo(a, j, remaining - a[j], current, out);
        current.pop_back();
    }
}

// O(k^(target/min)) time in the worst case, O(target/min) recursion space plus the output
vector<vector<long long>> combinationSum(vector<long long> candidates, long long target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<long long>> out;
    vector<long long> current;
    combinationSumGo(candidates, 0, target, current, out);
    return out;
}

int main() {
    cout << combinationSum(vector<long long>{2, 3, 6, 7}, 7) << endl;
    return 0;
}
