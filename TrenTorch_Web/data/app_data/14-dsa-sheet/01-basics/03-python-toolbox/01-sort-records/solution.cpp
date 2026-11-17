#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
vector<string> sortRecords(vector<pair<string, long long>> records) {
    sort(records.begin(), records.end(), [](const pair<string, long long>& a, const pair<string, long long>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    vector<string> names;
    names.reserve(records.size());
    for (const auto& r : records) names.push_back(r.first);
    return names;
}

int main() {
    return 0;
}
