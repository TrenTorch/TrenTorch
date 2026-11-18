#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long minPathSum(vector<vector<long long>> grid) {
    size_t rows = grid.size();
    size_t cols = rows ? grid[0].size() : 0;
    if (rows == 0 || cols == 0) return 0;
    vector<long long> row(cols, 0);
    for (size_t r = 0; r < rows; r++) {
        for (size_t c = 0; c < cols; c++) {
            if (r == 0 && c == 0) {
                row[c] = grid[0][0];
            } else if (r == 0) {
                row[c] = row[c - 1] + grid[r][c];
            } else if (c == 0) {
                row[c] = row[c] + grid[r][c];
            } else {
                row[c] = min(row[c], row[c - 1]) + grid[r][c];
            }
        }
    }
    return row[cols - 1];
}

int main() {
    cout << minPathSum(vector<vector<long long>>{vector<long long>{1, 3, 1}, vector<long long>{1, 5, 1}, vector<long long>{4, 2, 1}}) << endl;
    return 0;
}
