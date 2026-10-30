#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long uniquePathsObstacles(vector<vector<long long>> grid) {
    size_t rows = grid.size();
    size_t cols = rows ? grid[0].size() : 0;
    if (rows == 0 || cols == 0) return 0;
    const long long mod = 1000000007LL;
    vector<long long> row(cols, 0);
    row[0] = grid[0][0] == 0 ? 1 : 0;
    for (size_t r = 0; r < rows; r++) {
        for (size_t c = 0; c < cols; c++) {
            if (grid[r][c] == 1) {
                row[c] = 0;
            } else if (c > 0) {
                row[c] = (row[c] + row[c - 1]) % mod;
            }
        }
    }
    return row[cols - 1];
}

int main() {
    cout << uniquePathsObstacles(vector<vector<long long>>{vector<long long>{0, 0, 0}, vector<long long>{0, 1, 0}, vector<long long>{0, 0, 0}}) << endl;
    return 0;
}
