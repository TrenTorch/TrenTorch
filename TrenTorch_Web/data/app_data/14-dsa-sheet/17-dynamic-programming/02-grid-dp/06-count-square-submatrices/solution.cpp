#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long countSquares(vector<vector<long long>> matrix) {
    size_t rows = matrix.size();
    size_t cols = rows ? matrix[0].size() : 0;
    vector<long long> prev(cols + 1, 0);
    long long total = 0;
    for (size_t r = 0; r < rows; r++) {
        vector<long long> cur(cols + 1, 0);
        for (size_t c = 0; c < cols; c++) {
            if (matrix[r][c] == 1) {
                cur[c + 1] = 1 + min({prev[c], prev[c + 1], cur[c]});
                total += cur[c + 1];
            }
        }
        prev = cur;
    }
    return total;
}

int main() {
    cout << countSquares(vector<vector<long long>>{vector<long long>{0, 1, 1, 1}, vector<long long>{1, 1, 1, 1}, vector<long long>{0, 1, 1, 1}}) << endl;
    return 0;
}
