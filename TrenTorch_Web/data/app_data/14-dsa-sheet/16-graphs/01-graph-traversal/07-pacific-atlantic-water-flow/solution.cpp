#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R*C) space per flood (R rows, C cols)
vector<vector<bool>> floodFrom(const vector<vector<long long>>& heights, long long rows, long long cols,
                               const vector<pair<long long, long long>>& starts) {
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    vector<vector<bool>> seen(rows, vector<bool>(cols, false));
    vector<pair<long long, long long>> stack;
    for (const auto& s : starts) {
        seen[s.first][s.second] = true;
        stack.push_back(s);
    }
    while (!stack.empty()) {
        auto [x, y] = stack.back();
        stack.pop_back();
        for (int d = 0; d < 4; d++) {
            long long nx = x + dx[d];
            long long ny = y + dy[d];
            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && !seen[nx][ny] && heights[nx][ny] >= heights[x][y]) {
                seen[nx][ny] = true;
                stack.push_back({nx, ny});
            }
        }
    }
    return seen;
}

// O(R*C) time, O(R*C) space (R rows, C cols)
vector<vector<long long>> pacificAtlantic(vector<vector<long long>> heights) {
    long long rows = heights.size();
    long long cols = rows ? (long long)heights[0].size() : 0;
    if (rows == 0 || cols == 0) return {};
    vector<pair<long long, long long>> pacificStarts;
    vector<pair<long long, long long>> atlanticStarts;
    for (long long r = 0; r < rows; r++) {
        pacificStarts.push_back({r, 0});
        atlanticStarts.push_back({r, cols - 1});
    }
    for (long long c = 0; c < cols; c++) {
        pacificStarts.push_back({0, c});
        atlanticStarts.push_back({rows - 1, c});
    }
    vector<vector<bool>> pacific = floodFrom(heights, rows, cols, pacificStarts);
    vector<vector<bool>> atlantic = floodFrom(heights, rows, cols, atlanticStarts);
    vector<vector<long long>> result;
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            if (pacific[r][c] && atlantic[r][c]) result.push_back({r, c});
        }
    }
    return result;
}

int main() {
    cout << pacificAtlantic(vector<vector<long long>>{vector<long long>{1, 2}, vector<long long>{2, 1}}) << endl;
    return 0;
}
