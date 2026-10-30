#include <bits/stdc++.h>
using namespace std;

// O(log(rows * cols)) time, O(1) space
bool searchMatrix(vector<vector<long long>> matrix, long long target) {
    if (matrix.empty() || matrix[0].empty()) {
        return false;
    }
    long long rows = (long long)matrix.size(), cols = (long long)matrix[0].size();
    long long lo = 0, hi = rows * cols - 1;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        long long value = matrix[mid / cols][mid % cols];
        if (value == target) {
            return true;
        }
        if (value < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return false;
}

int main() {
    cout << boolalpha << searchMatrix(vector<vector<long long>>{vector<long long>{1, 3, 5, 7}, vector<long long>{10, 11, 16, 20}, vector<long long>{23, 30, 34, 60}}, 3) << endl;
    return 0;
}
