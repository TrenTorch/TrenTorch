#include <bits/stdc++.h>
using namespace std;

// O(rows^2) time, O(rows) space
long long minimumTotal(vector<vector<long long>> triangle) {
    if (triangle.empty()) return 0;
    vector<long long> best = triangle.back();
    for (int row = (int)triangle.size() - 2; row >= 0; row--) {
        for (int j = 0; j <= row; j++) {
            best[j] = triangle[row][j] + min(best[j], best[j + 1]);
        }
    }
    return best[0];
}

int main() {
    cout << minimumTotal(vector<vector<long long>>{vector<long long>{2}, vector<long long>{3, 4}, vector<long long>{6, 5, 7}, vector<long long>{4, 1, 8, 3}}) << endl;
    return 0;
}
