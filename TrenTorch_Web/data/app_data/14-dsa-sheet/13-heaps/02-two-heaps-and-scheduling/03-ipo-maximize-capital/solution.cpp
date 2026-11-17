#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long findMaximizedCapital(long long k, long long w, vector<long long> profits, vector<long long> capital) {
    vector<pair<long long, long long>> projects;  // (capital needed, profit)
    for (size_t i = 0; i < profits.size(); i++) projects.push_back({capital[i], profits[i]});
    sort(projects.begin(), projects.end());
    priority_queue<long long> heap;  // max-heap of affordable profits
    size_t i = 0;
    for (long long step = 0; step < k; step++) {
        while (i < projects.size() && projects[i].first <= w) {
            heap.push(projects[i].second);
            i++;
        }
        if (heap.empty()) break;
        w += heap.top();
        heap.pop();
    }
    return w;
}

int main() {
    cout << findMaximizedCapital(2, 0, vector<long long>{1, 2, 3}, vector<long long>{0, 1, 1}) << endl;
    return 0;
}
