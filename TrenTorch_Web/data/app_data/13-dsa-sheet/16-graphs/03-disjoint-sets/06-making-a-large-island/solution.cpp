#include <bits/stdc++.h>
using namespace std;

// O(R * C) time, O(R * C) space
long long largestIsland(vector<vector<long long>> grid) {
    int rows = grid.size();
    int cols = rows ? grid[0].size() : 0;
    vector<vector<int>> label(rows, vector<int>(cols, 0));
    vector<long long> size(1, 0);  // size[id] for island id; ids start at 1
    int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
    int nextId = 1;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 1 && label[r][c] == 0) {
                label[r][c] = nextId;
                vector<pair<int, int>> stk = {{r, c}};
                long long count = 0;
                while (!stk.empty()) {
                    auto [x, y] = stk.back();
                    stk.pop_back();
                    count++;
                    for (int k = 0; k < 4; k++) {
                        int nx = x + dx[k], ny = y + dy[k];
                        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols &&
                            grid[nx][ny] == 1 && label[nx][ny] == 0) {
                            label[nx][ny] = nextId;
                            stk.push_back({nx, ny});
                        }
                    }
                }
                size.push_back(count);
                nextId++;
            }
        }
    }
    long long best = 0;
    for (size_t i = 1; i < size.size(); i++) best = max(best, size[i]);
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 0) {
                set<int> around;
                for (int k = 0; k < 4; k++) {
                    int nx = r + dx[k], ny = c + dy[k];
                    if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && label[nx][ny] != 0) {
                        around.insert(label[nx][ny]);
                    }
                }
                long long total = 1;
                for (int id : around) total += size[id];
                best = max(best, total);
            }
        }
    }
    return best;
}

int main() {
    cout << largestIsland(vector<vector<long long>>{vector<long long>{1, 0}, vector<long long>{0, 1}}) << endl;
    return 0;
}
