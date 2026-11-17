#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(4^(R*C)) worst-case time (all simple paths are explored), O(R*C) space
vector<string> ratInAMaze(vector<vector<long long>> maze) {
    int rows = maze.size();
    int cols = rows ? maze[0].size() : 0;
    vector<string> out;
    if (rows == 0 || cols == 0 || maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0) return out;
    struct Move {
        char letter;
        int dr;
        int dc;
    };
    const Move moves[] = {{'D', 1, 0}, {'L', 0, -1}, {'R', 0, 1}, {'U', -1, 0}};
    string path;
    vector<vector<bool>> onPath(rows, vector<bool>(cols, false));
    function<void(int, int)> go = [&](int r, int c) {
        if (r == rows - 1 && c == cols - 1) {
            out.push_back(path);
            return;
        }
        onPath[r][c] = true;
        for (const Move& m : moves) {
            int nr = r + m.dr;
            int nc = c + m.dc;
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] == 1 && !onPath[nr][nc]) {
                path.push_back(m.letter);
                go(nr, nc);
                path.pop_back();
            }
        }
        onPath[r][c] = false;
    };
    go(0, 0);
    return out;
}

int main() {
    cout << ratInAMaze(vector<vector<long long>>{vector<long long>{1, 0, 0, 0}, vector<long long>{1, 1, 0, 1}, vector<long long>{1, 1, 0, 0}, vector<long long>{0, 1, 1, 1}}) << endl;
    return 0;
}
