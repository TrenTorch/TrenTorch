#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// Backtracking with minimum-remaining-values choice: exponential worst case, O(81) space plus recursion depth
vector<vector<long long>> sudokuSolver(vector<vector<long long>> board) {
    vector<set<long long>> rows(9), cols(9), boxes(9);
    vector<pair<int, int>> empty;
    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            long long v = board[r][c];
            if (v) {
                rows[r].insert(v);
                cols[c].insert(v);
                boxes[r / 3 * 3 + c / 3].insert(v);
            } else {
                empty.push_back({r, c});
            }
        }
    }

    auto candidates = [&](int r, int c) {
        set<long long> options;
        for (long long v = 1; v <= 9; v++) {
            if (!rows[r].count(v) && !cols[c].count(v) && !boxes[r / 3 * 3 + c / 3].count(v)) options.insert(v);
        }
        return options;
    };

    function<bool()> go = [&]() -> bool {
        bool hasBest = false;
        int bestR = 0, bestC = 0;
        set<long long> bestOptions;
        for (auto [r, c] : empty) {
            if (board[r][c] == 0) {
                set<long long> options = candidates(r, c);
                if (!hasBest || options.size() < bestOptions.size()) {
                    hasBest = true;
                    bestR = r;
                    bestC = c;
                    bestOptions = options;
                    if (options.size() <= 1) break;
                }
            }
        }
        if (!hasBest) return true;
        for (long long v : bestOptions) {
            board[bestR][bestC] = v;
            rows[bestR].insert(v);
            cols[bestC].insert(v);
            boxes[bestR / 3 * 3 + bestC / 3].insert(v);
            if (go()) return true;
            board[bestR][bestC] = 0;
            rows[bestR].erase(v);
            cols[bestC].erase(v);
            boxes[bestR / 3 * 3 + bestC / 3].erase(v);
        }
        return false;
    };

    go();
    return board;
}

int main() {
    cout << sudokuSolver(vector<vector<long long>>{vector<long long>{5, 3, 0, 0, 7, 0, 0, 0, 0}, vector<long long>{6, 0, 0, 1, 9, 5, 0, 0, 0}, vector<long long>{0, 9, 8, 0, 0, 0, 0, 6, 0}, vector<long long>{8, 0, 0, 0, 6, 0, 0, 0, 3}, vector<long long>{4, 0, 0, 8, 0, 3, 0, 0, 1}, vector<long long>{7, 0, 0, 0, 2, 0, 0, 0, 6}, vector<long long>{0, 6, 0, 0, 0, 0, 2, 8, 0}, vector<long long>{0, 0, 0, 4, 1, 9, 0, 0, 5}, vector<long long>{0, 0, 0, 0, 8, 0, 0, 7, 9}}) << endl;
    return 0;
}
