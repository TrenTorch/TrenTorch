#include <bits/stdc++.h>
using namespace std;

// O(rows * log(max - min)) time, O(1) extra space
long long kthSmallestMatrix(vector<vector<long long>> matrix, long long k) {
    long long rows = (long long)matrix.size();
    long long cols = (long long)matrix[0].size();

    auto countAtMost = [&](long long x) {
        long long count = 0;
        long long col = cols - 1;
        for (long long r = 0; r < rows; r++) {
            while (col >= 0 && matrix[r][col] > x) col--;
            count += col + 1;
        }
        return count;
    };

    long long lo = matrix[0][0];
    long long hi = matrix[rows - 1][cols - 1];
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;  // same as Python's floor((lo + hi) / 2)
        if (countAtMost(mid) >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

int main() {
    cout << kthSmallestMatrix(vector<vector<long long>>{vector<long long>{1, 5, 9}, vector<long long>{10, 11, 13}, vector<long long>{12, 13, 15}}, 8) << endl;
    return 0;
}
