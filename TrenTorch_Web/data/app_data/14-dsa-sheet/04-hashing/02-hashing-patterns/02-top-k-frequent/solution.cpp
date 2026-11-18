#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) expected time to count, O(d) expected time for the random-pivot selection,
// O(d log d) for the final sort of the chosen pairs (d = distinct values), O(d) space
vector<long long> topKFrequent(vector<long long> nums, long long k) {
    unordered_map<long long, long long> counts;
    counts.reserve(nums.size() * 2 + 1);
    for (long long x : nums) counts[x]++;
    vector<pair<long long, long long>> pairs;  // (-count, value)
    for (const auto& [value, count] : counts) pairs.push_back({-count, value});
    if (k <= 0) return {};
    if (k < (long long)pairs.size()) {
        vector<pair<long long, long long>> chosen;
        vector<pair<long long, long long>> pool = pairs;
        long long need = k;
        mt19937 rng(random_device{}());
        while (need > 0) {
            pair<long long, long long> pivot = pool[rng() % pool.size()];
            vector<pair<long long, long long>> less;
            for (const auto& p : pool) {
                if (p < pivot) less.push_back(p);
            }
            long long L = (long long)less.size();
            if (need <= L) {
                pool = less;
            } else if (need == L + 1) {
                chosen.insert(chosen.end(), less.begin(), less.end());
                chosen.push_back(pivot);
                need = 0;
            } else {
                chosen.insert(chosen.end(), less.begin(), less.end());
                chosen.push_back(pivot);
                need -= L + 1;
                vector<pair<long long, long long>> greater;
                for (const auto& p : pool) {
                    if (p > pivot) greater.push_back(p);
                }
                pool = greater;
            }
        }
        pairs = chosen;
    }
    sort(pairs.begin(), pairs.end());
    vector<long long> out;
    for (const auto& [negCount, value] : pairs) out.push_back(value);
    return out;
}

int main() {
    cout << topKFrequent(vector<long long>{1, 1, 1, 2, 2, 3}, 2) << endl;
    return 0;
}
