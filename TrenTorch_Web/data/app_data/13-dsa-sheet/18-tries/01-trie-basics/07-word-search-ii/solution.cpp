#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R * C * 4^L + total word length) time, O(total word length * 26) space
vector<string> findWords(vector<string> board, vector<string> words) {
    int rows = board.size();
    int cols = rows ? static_cast<int>(board[0].size()) : 0;
    vector<array<int, 26>> nxt(1);
    nxt[0].fill(-1);
    vector<bool> isEnd(1, false);
    vector<string> endWord(1);
    for (const string& w : words) {
        int node = 0;
        for (char c : w) {
            int id = c - 'a';
            if (nxt[node][id] < 0) {
                nxt[node][id] = static_cast<int>(nxt.size());
                array<int, 26> fresh;
                fresh.fill(-1);
                nxt.push_back(fresh);
                isEnd.push_back(false);
                endWord.push_back("");
            }
            node = nxt[node][id];
        }
        isEnd[node] = true;
        endWord[node] = w;
    }
    vector<string> grid = board;
    set<string> found;
    const int dr[4] = {1, -1, 0, 0};
    const int dc[4] = {0, 0, 1, -1};
    function<void(int, int, int)> dfs = [&](int r, int c, int node) {
        char ch = grid[r][c];
        int nxtNode = nxt[node][ch - 'a'];
        if (nxtNode < 0) return;
        if (isEnd[nxtNode]) found.insert(endWord[nxtNode]);
        grid[r][c] = '#';
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d];
            int nc = c + dc[d];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != '#') {
                dfs(nr, nc, nxtNode);
            }
        }
        grid[r][c] = ch;
    };
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) dfs(r, c, 0);
    }
    return vector<string>(found.begin(), found.end());
}

int main() {
    cout << findWords(vector<string>{"oaan", "etae", "ihkr", "iflv"}, vector<string>{"oath", "pea", "eat", "rain"}) << endl;
    return 0;
}
