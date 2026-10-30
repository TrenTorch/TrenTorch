#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time, O(n) space
vector<vector<long long>> mergeIntervals(vector<vector<long long>> intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<long long>> out;
    for (const auto& iv : intervals) {
        long long start = iv[0], end = iv[1];
        if (!out.empty() && start <= out.back()[1]) {
            out.back()[1] = max(out.back()[1], end);
        } else {
            out.push_back({start, end});
        }
    }
    return out;
}

int main() {
    cout << mergeIntervals(vector<vector<long long>>{vector<long long>{1, 3}, vector<long long>{8, 10}, vector<long long>{2, 6}, vector<long long>{15, 18}}) << endl;
    return 0;
}
