#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long maxActivities(vector<long long> starts, vector<long long> ends) {
    vector<pair<long long, long long>> acts;
    acts.reserve(starts.size());
    for (size_t i = 0; i < starts.size(); i++) {
        acts.push_back({ends[i], starts[i]});
    }
    sort(acts.begin(), acts.end());
    long long count = 0;
    long long lastEnd = -1;
    for (const auto& act : acts) {
        long long end = act.first;
        long long start = act.second;
        if (start >= lastEnd) {
            count++;
            lastEnd = end;
        }
    }
    return count;
}

int main() {
    cout << maxActivities(vector<long long>{1, 3, 0, 5, 8, 5}, vector<long long>{2, 4, 6, 7, 9, 9}) << endl;
    return 0;
}
