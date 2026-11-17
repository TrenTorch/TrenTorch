#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R*C) space (R rows, C cols)
vector<vector<long long>> floodFill(vector<vector<long long>> image, long long sr, long long sc, long long color) {
    long long old = image[sr][sc];
    if (old == color) return image;
    long long rows = image.size();
    long long cols = image[0].size();
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    image[sr][sc] = color;
    vector<pair<long long, long long>> stack = {{sr, sc}};
    while (!stack.empty()) {
        auto [x, y] = stack.back();
        stack.pop_back();
        for (int d = 0; d < 4; d++) {
            long long nx = x + dx[d];
            long long ny = y + dy[d];
            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && image[nx][ny] == old) {
                image[nx][ny] = color;
                stack.push_back({nx, ny});
            }
        }
    }
    return image;
}

int main() {
    cout << floodFill(vector<vector<long long>>{vector<long long>{1, 1, 1}, vector<long long>{1, 1, 0}, vector<long long>{1, 0, 1}}, 1, 1, 2) << endl;
    return 0;
}
