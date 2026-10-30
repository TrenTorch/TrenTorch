#include <bits/stdc++.h>
using namespace std;

// O(rows * cols) time, O(cols) space
long long calculateMinimumHp(vector<vector<long long>> dungeon) {
    size_t rows = dungeon.size();
    size_t cols = rows ? dungeon[0].size() : 0;
    if (rows == 0 || cols == 0) return 1;
    const long long INF = LLONG_MAX / 4;
    vector<long long> need(cols + 1, INF);
    need[cols - 1] = 1;
    for (int r = (int)rows - 1; r >= 0; r--) {
        for (int c = (int)cols - 1; c >= 0; c--) {
            long long bestNext = min(need[c], need[c + 1]);
            if (r == (int)rows - 1 && c == (int)cols - 1) bestNext = 1;
            need[c] = max(1LL, bestNext - dungeon[r][c]);
        }
        need[cols] = INF;
    }
    return need[0];
}

int main() {
    cout << calculateMinimumHp(vector<vector<long long>>{vector<long long>{-2, -3, 3}, vector<long long>{-5, -10, 1}, vector<long long>{10, 30, -5}}) << endl;
    return 0;
}
