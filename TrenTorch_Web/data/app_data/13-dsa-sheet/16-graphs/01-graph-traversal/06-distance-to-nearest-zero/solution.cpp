#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R*C) space (R rows, C cols)
vector<vector<long long>> nearestZero(vector<vector<long long>> mat) {
    long long rows = mat.size();
    long long cols = rows ? (long long)mat[0].size() : 0;
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    vector<vector<long long>> dist(rows, vector<long long>(cols, -1));
    deque<pair<long long, long long>> q;
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            if (mat[r][c] == 0) {
                dist[r][c] = 0;
                q.push_back({r, c});
            }
        }
    }
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop_front();
        for (int d = 0; d < 4; d++) {
            long long nx = x + dx[d];
            long long ny = y + dy[d];
            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && dist[nx][ny] == -1) {
                dist[nx][ny] = dist[x][y] + 1;
                q.push_back({nx, ny});
            }
        }
    }
    return dist;
}

int main() {
    cout << nearestZero(vector<vector<long long>>{vector<long long>{0, 0, 0}, vector<long long>{0, 1, 0}, vector<long long>{1, 1, 1}}) << endl;
    return 0;
}
