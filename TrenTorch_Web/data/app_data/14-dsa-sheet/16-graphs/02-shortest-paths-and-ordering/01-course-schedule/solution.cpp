#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(n + m) space (m = number of prerequisites)
bool canFinish(long long numCourses, vector<vector<long long>> prerequisites) {
    vector<vector<long long>> adj(numCourses);
    vector<long long> inDegree(numCourses, 0);
    for (const auto& p : prerequisites) {
        adj[p[1]].push_back(p[0]);
        inDegree[p[0]]++;
    }
    deque<long long> queue;
    for (long long v = 0; v < numCourses; v++) {
        if (inDegree[v] == 0) queue.push_back(v);
    }
    long long taken = 0;
    while (!queue.empty()) {
        long long node = queue.front();
        queue.pop_front();
        taken++;
        for (long long nxt : adj[node]) {
            inDegree[nxt]--;
            if (inDegree[nxt] == 0) queue.push_back(nxt);
        }
    }
    return taken == numCourses;
}

int main() {
    cout << boolalpha << canFinish(2, vector<vector<long long>>{vector<long long>{1, 0}}) << endl;
    return 0;
}
