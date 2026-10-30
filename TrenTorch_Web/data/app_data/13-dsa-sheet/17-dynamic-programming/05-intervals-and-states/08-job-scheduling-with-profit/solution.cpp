#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long jobScheduling(vector<vector<long long>> jobs) {
    stable_sort(jobs.begin(), jobs.end(), [](const vector<long long>& a, const vector<long long>& b) {
        return a[1] < b[1];
    });
    int n = jobs.size();
    vector<long long> ends(n);
    for (int i = 0; i < n; i++) ends[i] = jobs[i][1];
    vector<long long> best(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long start = jobs[i - 1][0];
        long long profit = jobs[i - 1][2];
        int before = upper_bound(ends.begin(), ends.begin() + (i - 1), start) - ends.begin();
        best[i] = max(best[i - 1], profit + best[before]);
    }
    return best[n];
}

int main() {
    cout << jobScheduling(vector<vector<long long>>{vector<long long>{1, 3, 50}, vector<long long>{2, 4, 10}, vector<long long>{3, 5, 40}, vector<long long>{3, 6, 70}}) << endl;
    return 0;
}
