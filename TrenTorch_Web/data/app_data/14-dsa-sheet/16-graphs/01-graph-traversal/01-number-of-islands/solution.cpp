#include <bits/stdc++.h>
using namespace std;

// O(R*C) time, O(R*C) space (R rows, C cols)
long long numIslands(vector<vector<long long>> grid) {
    long long rows = grid.size();
    long long cols = rows ? (long long)grid[0].size() : 0;
    vector<vector<bool>> seen(rows, vector<bool>(cols, false));
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    long long count = 0;
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            if (grid[r][c] == 1 && !seen[r][c]) {
                count++;
                seen[r][c] = true;
                vector<pair<long long, long long>> stack = {{r, c}};
                while (!stack.empty()) {
                    auto [x, y] = stack.back();
                    stack.pop_back();
                    for (int d = 0; d < 4; d++) {
                        long long nx = x + dx[d];
                        long long ny = y + dy[d];
                        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && grid[nx][ny] == 1 && !seen[nx][ny]) {
                            seen[nx][ny] = true;
                            stack.push_back({nx, ny});
                        }
                    }
                }
            }
        }
    }
    return count;
}

int main() {
    cout << numIslands(vector<vector<long long>>{vector<long long>{1, 1, 0}, vector<long long>{0, 1, 0}, vector<long long>{0, 0, 1}}) << endl;
    return 0;
}
