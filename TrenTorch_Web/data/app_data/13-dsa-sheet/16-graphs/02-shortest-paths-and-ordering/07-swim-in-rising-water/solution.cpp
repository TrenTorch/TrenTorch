#include <bits/stdc++.h>
using namespace std;

// O(N log N) time, O(N) space (N = number of cells)
long long swimInWater(vector<vector<long long>> grid) {
    int n = grid.size(), m = grid[0].size();
    vector<vector<bool>> seen(n, vector<bool>(m, false));
    using State = tuple<long long, int, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    heap.push({grid[0][0], 0, 0});
    seen[0][0] = true;
    int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
    while (!heap.empty()) {
        auto [t, x, y] = heap.top();
        heap.pop();
        if (x == n - 1 && y == m - 1) return t;
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx >= 0 && nx < n && ny >= 0 && ny < m && !seen[nx][ny]) {
                seen[nx][ny] = true;
                heap.push({max(t, grid[nx][ny]), nx, ny});
            }
        }
    }
    return 0;
}

int main() {
    cout << swimInWater(vector<vector<long long>>{vector<long long>{0, 2}, vector<long long>{1, 3}}) << endl;
    return 0;
}
