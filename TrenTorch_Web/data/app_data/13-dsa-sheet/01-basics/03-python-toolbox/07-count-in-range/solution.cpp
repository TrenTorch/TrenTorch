#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + q log n) time, O(q) space for the answers (binary search per query)
vector<long long> countInRange(vector<long long> sortedNums, vector<vector<long long>> queries) {
    vector<long long> answers;
    answers.reserve(queries.size());
    for (const auto& q : queries) {
        auto lo = lower_bound(sortedNums.begin(), sortedNums.end(), q[0]);
        auto hi = upper_bound(sortedNums.begin(), sortedNums.end(), q[1]);
        answers.push_back((long long)(hi - lo));
    }
    return answers;
}

int main() {
    cout << countInRange(vector<long long>{1, 3, 3, 5, 8}, vector<vector<long long>>{vector<long long>{3, 5}, vector<long long>{0, 0}, vector<long long>{2, 9}}) << endl;
    return 0;
}
