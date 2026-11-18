#include <bits/stdc++.h>
using namespace std;

long long largestInHistogram(const vector<long long>& hs) {
    int n = hs.size();
    long long result = 0;
    vector<int> stack;
    for (int i = 0; i <= n; i++) {
        long long h = (i == n) ? 0 : hs[i];
        while (!stack.empty() && hs[stack.back()] >= h) {
            long long height = hs[stack.back()];
            stack.pop_back();
            int left = stack.empty() ? -1 : stack.back();
            result = max(result, height * (long long)(i - left - 1));
        }
        stack.push_back(i);
    }
    return result;
}

// O(rows * cols) time, O(cols) space
long long maximalRectangle(vector<vector<long long>> matrix) {
    if (matrix.empty()) return 0;
    int cols = matrix[0].size();
    vector<long long> heights(cols, 0);
    long long best = 0;
    for (const auto& row : matrix) {
        for (int j = 0; j < cols; j++) {
            heights[j] = row[j] ? heights[j] + 1 : 0;
        }
        best = max(best, largestInHistogram(heights));
    }
    return best;
}

int main() {
    cout << maximalRectangle(vector<vector<long long>>{vector<long long>{1, 0, 1, 0, 0}, vector<long long>{1, 0, 1, 1, 1}, vector<long long>{1, 1, 1, 1, 1}, vector<long long>{1, 0, 0, 1, 0}}) << endl;
    return 0;
}
