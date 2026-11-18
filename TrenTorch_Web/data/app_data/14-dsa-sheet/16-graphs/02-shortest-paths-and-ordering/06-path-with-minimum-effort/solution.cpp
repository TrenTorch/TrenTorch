#include <bits/stdc++.h>
using namespace std;

// O(R*C log(R*C)) time, O(R*C) space
long long minimumEffortPath(vector<vector<long long>> heights) {
    int rows = heights.size(), cols = heights[0].size();
    const long long INF = LLONG_MAX;
    vector<vector<long long>> effort(rows, vector<long long>(cols, INF));
    effort[0][0] = 0;
    using State = tuple<long long, int, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    heap.push({0, 0, 0});
    int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
    while (!heap.empty()) {
        auto [e, x, y] = heap.top();
        heap.pop();
        if (x == rows - 1 && y == cols - 1) return e;
        if (e > effort[x][y]) continue;
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols) {
                long long ne = max(e, llabs(heights[nx][ny] - heights[x][y]));
                if (ne < effort[nx][ny]) {
                    effort[nx][ny] = ne;
                    heap.push({ne, nx, ny});
                }
            }
        }
    }
    return 0;
}

int main() {
    cout << minimumEffortPath(vector<vector<long long>>{vector<long long>{1, 2, 2}, vector<long long>{3, 8, 2}, vector<long long>{5, 3, 5}}) << endl;
    return 0;
}
