#include <bits/stdc++.h>
using namespace std;

// O(R*C) time, O(R*C) space (R rows, C cols)
long long shortestPathBinaryMatrix(vector<vector<long long>> grid) {
    long long rows = grid.size();
    long long cols = rows ? (long long)grid[0].size() : 0;
    if (rows == 0 || cols == 0 || grid[0][0] == 1 || grid[rows - 1][cols - 1] == 1) return -1;
    vector<vector<bool>> seen(rows, vector<bool>(cols, false));
    seen[0][0] = true;
    deque<tuple<long long, long long, long long>> q;
    q.push_back({0, 0, 1});
    while (!q.empty()) {
        auto [x, y, steps] = q.front();
        q.pop_front();
        if (x == rows - 1 && y == cols - 1) return steps;
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                long long nx = x + dx;
                long long ny = y + dy;
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 0 && !seen[nx][ny]) {
                    seen[nx][ny] = true;
                    q.push_back({nx, ny, steps + 1});
                }
            }
        }
    }
    return -1;
}

int main() {
    cout << shortestPathBinaryMatrix(vector<vector<long long>>{vector<long long>{0, 0, 0}, vector<long long>{1, 1, 0}, vector<long long>{1, 1, 0}}) << endl;
    return 0;
}
