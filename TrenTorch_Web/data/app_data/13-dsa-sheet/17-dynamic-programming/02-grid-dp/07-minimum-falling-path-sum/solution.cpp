#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long minFallingPathSum(vector<vector<long long>> matrix) {
    if (matrix.empty() || matrix[0].empty()) return 0;
    size_t cols = matrix[0].size();
    vector<long long> prev = matrix[0];
    for (size_t r = 1; r < matrix.size(); r++) {
        vector<long long> cur(cols, 0);
        for (size_t c = 0; c < cols; c++) {
            size_t lo = c > 0 ? c - 1 : 0;
            size_t hi = min(cols - 1, c + 1);
            long long best = prev[lo];
            for (size_t k = lo + 1; k <= hi; k++) best = min(best, prev[k]);
            cur[c] = matrix[r][c] + best;
        }
        prev = cur;
    }
    return *min_element(prev.begin(), prev.end());
}

int main() {
    cout << minFallingPathSum(vector<vector<long long>>{vector<long long>{2, 1, 3}, vector<long long>{6, 5, 4}, vector<long long>{7, 8, 9}}) << endl;
    return 0;
}
