#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((n + m) log n) time, O(n + m) space (m = number of prerequisites)
vector<long long> findOrder(long long numCourses, vector<vector<long long>> prerequisites) {
    vector<vector<long long>> adj(numCourses);
    vector<long long> inDegree(numCourses, 0);
    for (const auto& p : prerequisites) {
        adj[p[1]].push_back(p[0]);
        inDegree[p[0]]++;
    }
    priority_queue<long long, vector<long long>, greater<long long>> heap;
    for (long long v = 0; v < numCourses; v++) {
        if (inDegree[v] == 0) heap.push(v);
    }
    vector<long long> order;
    while (!heap.empty()) {
        long long node = heap.top();
        heap.pop();
        order.push_back(node);
        for (long long nxt : adj[node]) {
            inDegree[nxt]--;
            if (inDegree[nxt] == 0) heap.push(nxt);
        }
    }
    if ((long long)order.size() != numCourses) return {};
    return order;
}

int main() {
    cout << findOrder(4, vector<vector<long long>>{vector<long long>{1, 0}, vector<long long>{2, 0}, vector<long long>{3, 1}, vector<long long>{3, 2}}) << endl;
    return 0;
}
