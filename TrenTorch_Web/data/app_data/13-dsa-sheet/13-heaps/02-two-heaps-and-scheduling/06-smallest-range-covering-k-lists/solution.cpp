#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(N log k) time, O(k) space where N is the total number of values
vector<long long> smallestRange(vector<vector<long long>> lists) {
    using Node = tuple<long long, size_t, size_t>;  // (value, list index, position)
    priority_queue<Node, vector<Node>, greater<Node>> heap;
    long long currentMax = LLONG_MIN;
    for (size_t i = 0; i < lists.size(); i++) {
        heap.emplace(lists[i][0], i, 0);
        currentMax = max(currentMax, lists[i][0]);
    }
    vector<long long> best = {get<0>(heap.top()), currentMax};
    while (true) {
        auto [value, i, j] = heap.top();
        heap.pop();
        if (make_pair(currentMax - value, value) < make_pair(best[1] - best[0], best[0])) {
            best = {value, currentMax};
        }
        if (j + 1 == lists[i].size()) return best;
        long long nxt = lists[i][j + 1];
        currentMax = max(currentMax, nxt);
        heap.emplace(nxt, i, j + 1);
    }
}

int main() {
    cout << smallestRange(vector<vector<long long>>{vector<long long>{4, 10, 15, 24, 26}, vector<long long>{0, 9, 12, 20}, vector<long long>{5, 18, 22, 30}}) << endl;
    return 0;
}
