#include <bits/stdc++.h>
using namespace std;

// O(R * C * 4^L) time worst case (R, C grid size, L word length), O(L) recursion depth
bool wordSearch(vector<string> board, string word) {
    if (word.empty()) return true;
    int rows = board.size();
    int cols = rows ? board[0].size() : 0;
    function<bool(int, int, size_t)> go = [&](int r, int c, size_t i) -> bool {
        if (i == word.size()) return true;
        if (!(r >= 0 && r < rows && c >= 0 && c < cols) || board[r][c] != word[i]) return false;
        char saved = board[r][c];
        board[r][c] = '#';
        bool found = go(r + 1, c, i + 1) || go(r - 1, c, i + 1) || go(r, c + 1, i + 1) || go(r, c - 1, i + 1);
        board[r][c] = saved;
        return found;
    };
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (go(r, c, 0)) return true;
        }
    }
    return false;
}

int main() {
    cout << boolalpha << wordSearch(vector<string>{"abce", "sfcs", "adee"}, "abcced") << endl;
    return 0;
}
