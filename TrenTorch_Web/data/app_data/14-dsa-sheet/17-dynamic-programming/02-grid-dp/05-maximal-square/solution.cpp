#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long maximalSquare(vector<vector<long long>> matrix) {
    size_t rows = matrix.size();
    size_t cols = rows ? matrix[0].size() : 0;
    vector<long long> prev(cols + 1, 0);
    long long best = 0;
    for (size_t r = 0; r < rows; r++) {
        vector<long long> cur(cols + 1, 0);
        for (size_t c = 0; c < cols; c++) {
            if (matrix[r][c] == 1) {
                cur[c + 1] = 1 + min({prev[c], prev[c + 1], cur[c]});
                best = max(best, cur[c + 1]);
            }
        }
        prev = cur;
    }
    return best * best;
}

int main() {
    cout << maximalSquare(vector<vector<long long>>{vector<long long>{1, 0, 1, 0, 0}, vector<long long>{1, 0, 1, 1, 1}, vector<long long>{1, 1, 1, 1, 1}, vector<long long>{1, 0, 0, 1, 0}}) << endl;
    return 0;
}
