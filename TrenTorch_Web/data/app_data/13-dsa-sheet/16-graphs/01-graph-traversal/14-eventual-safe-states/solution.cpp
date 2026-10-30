#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + m) time, O(n + m) space (m = number of edges)
vector<long long> eventualSafeNodes(long long n, vector<vector<long long>> edges) {
    vector<vector<long long>> rev(n);
    vector<long long> outDegree(n, 0);
    for (const auto& e : edges) {
        rev[e[1]].push_back(e[0]);
        outDegree[e[0]]++;
    }
    deque<long long> queue;
    for (long long v = 0; v < n; v++) {
        if (outDegree[v] == 0) queue.push_back(v);
    }
    vector<bool> safe(n, false);
    while (!queue.empty()) {
        long long node = queue.front();
        queue.pop_front();
        safe[node] = true;
        for (long long p : rev[node]) {
            outDegree[p]--;
            if (outDegree[p] == 0) queue.push_back(p);
        }
    }
    vector<long long> result;
    for (long long v = 0; v < n; v++) {
        if (safe[v]) result.push_back(v);
    }
    return result;
}

int main() {
    cout << eventualSafeNodes(7, vector<vector<long long>>{vector<long long>{0, 1}, vector<long long>{0, 2}, vector<long long>{1, 2}, vector<long long>{1, 3}, vector<long long>{2, 5}, vector<long long>{3, 0}, vector<long long>{4, 5}}) << endl;
    return 0;
}
