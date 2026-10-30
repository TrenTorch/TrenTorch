#include <bits/stdc++.h>
using namespace std;

// O(R*C) time, O(R*C) space (R rows, C cols)
long long orangesRotting(vector<vector<long long>> grid) {
    long long rows = grid.size();
    long long cols = rows ? (long long)grid[0].size() : 0;
    vector<vector<long long>> g = grid;
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    deque<pair<long long, long long>> q;
    long long fresh = 0;
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            if (g[r][c] == 2) {
                q.push_back({r, c});
            } else if (g[r][c] == 1) {
                fresh++;
            }
        }
    }
    long long minutes = 0;
    while (!q.empty() && fresh) {
        minutes++;
        size_t level = q.size();
        for (size_t k = 0; k < level; k++) {
            auto [x, y] = q.front();
            q.pop_front();
            for (int d = 0; d < 4; d++) {
                long long nx = x + dx[d];
                long long ny = y + dy[d];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && g[nx][ny] == 1) {
                    g[nx][ny] = 2;
                    fresh--;
                    q.push_back({nx, ny});
                }
            }
        }
    }
    return fresh == 0 ? minutes : -1;
}

int main() {
    cout << orangesRotting(vector<vector<long long>>{vector<long long>{2, 1, 1}, vector<long long>{1, 1, 0}, vector<long long>{0, 1, 1}}) << endl;
    return 0;
}
