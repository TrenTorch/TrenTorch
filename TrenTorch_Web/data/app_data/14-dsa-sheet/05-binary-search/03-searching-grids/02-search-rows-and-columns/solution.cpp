#include <bits/stdc++.h>
using namespace std;

// Looks for target in rows r0..r1 and columns c0..c1 (both inclusive).
bool searchRowsAndColumnsRange(const vector<vector<long long>>& matrix, long long target,
                               long long r0, long long r1, long long c0, long long c1) {
    if (r0 > r1 || c0 > c1) {
        return false;
    }
    if (r1 - r0 <= c1 - c0) {
        long long r = (r0 + r1) / 2;
        long long lo = c0, hi = c1 + 1;
        while (lo < hi) {
            long long mid = (lo + hi) / 2;
            if (matrix[r][mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if (lo <= c1 && matrix[r][lo] == target) {
            return true;
        }
        return searchRowsAndColumnsRange(matrix, target, r0, r - 1, lo, c1) ||
               searchRowsAndColumnsRange(matrix, target, r + 1, r1, c0, lo - 1);
    }
    long long c = (c0 + c1) / 2;
    long long lo = r0, hi = r1 + 1;
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (matrix[mid][c] < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if (lo <= r1 && matrix[lo][c] == target) {
        return true;
    }
    return searchRowsAndColumnsRange(matrix, target, r0, lo - 1, c + 1, c1) ||
           searchRowsAndColumnsRange(matrix, target, lo, r1, c0, c - 1);
}

// O(rows + cols) time per halving step, O(min(rows, cols)) recursion depth
bool searchMatrixIi(vector<vector<long long>> matrix, long long target) {
    if (matrix.empty() || matrix[0].empty()) {
        return false;
    }
    return searchRowsAndColumnsRange(matrix, target, 0, (long long)matrix.size() - 1,
                                     0, (long long)matrix[0].size() - 1);
}

int main() {
    cout << boolalpha << searchMatrixIi(vector<vector<long long>>{vector<long long>{1, 4, 7, 11}, vector<long long>{2, 5, 8, 12}, vector<long long>{3, 6, 9, 16}, vector<long long>{10, 13, 14, 17}}, 5) << endl;
    return 0;
}
