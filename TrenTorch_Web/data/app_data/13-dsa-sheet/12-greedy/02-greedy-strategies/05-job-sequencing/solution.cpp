#include <bits/stdc++.h>
using namespace std;

// O(n log n + n * alpha(D)) time, O(D) space where D = min(max deadline, n)
long long maxJobProfit(vector<vector<long long>> jobs) {
    long long maxDeadline = 0;
    for (const auto& j : jobs) maxDeadline = max(maxDeadline, j[0]);
    long long limit = min(maxDeadline, (long long)jobs.size());

    // DSU over time slots 0..limit; find(t) gives the latest free slot <= t (0 means none)
    vector<long long> parent(limit + 1);
    iota(parent.begin(), parent.end(), 0LL);
    auto findSlot = [&](long long t) {
        while (parent[t] != t) {
            parent[t] = parent[parent[t]];
            t = parent[t];
        }
        return t;
    };

    stable_sort(jobs.begin(), jobs.end(), [](const vector<long long>& a, const vector<long long>& b) {
        return a[1] > b[1];
    });

    long long total = 0;
    for (const auto& j : jobs) {
        long long slot = findSlot(min(j[0], limit));
        if (slot > 0) {
            parent[slot] = slot - 1;
            total += j[1];
        }
    }
    return total;
}

int main() {
    cout << maxJobProfit(vector<vector<long long>>{vector<long long>{4, 20}, vector<long long>{1, 10}, vector<long long>{1, 40}, vector<long long>{1, 30}}) << endl;
    return 0;
}
