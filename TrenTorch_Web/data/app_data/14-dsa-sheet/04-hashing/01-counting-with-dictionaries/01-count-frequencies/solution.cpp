#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + q) expected time, O(n) space
vector<long long> countFrequencies(vector<long long> nums, vector<long long> queries) {
    unordered_map<long long, long long> counts;
    counts.reserve(nums.size() * 2 + 1);
    for (long long x : nums) counts[x]++;
    vector<long long> out;
    out.reserve(queries.size());
    for (long long q : queries) {
        auto it = counts.find(q);
        out.push_back(it == counts.end() ? 0 : it->second);
    }
    return out;
}

int main() {
    cout << countFrequencies(vector<long long>{1, 2, 2, 3, 3, 3}, vector<long long>{3, 2, 5}) << endl;
    return 0;
}
