#include <bits/stdc++.h>
using namespace std;

// O(1) time (fixed 9x9 board), O(1) space (at most 243 stored keys)
bool validSudoku(vector<vector<long long>> board) {
    set<tuple<int, int, long long>> seen;
    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            long long digit = board[r][c];
            if (digit == 0) continue;
            tuple<int, int, long long> keys[3] = {
                make_tuple(0, r, digit),
                make_tuple(1, c, digit),
                make_tuple(2, (r / 3) * 3 + c / 3, digit),
            };
            for (const auto& key : keys) {
                if (seen.count(key)) return false;
            }
            for (const auto& key : keys) seen.insert(key);
        }
    }
    return true;
}

int main() {
    cout << boolalpha << validSudoku(vector<vector<long long>>{vector<long long>{5, 3, 0, 0, 7, 0, 0, 0, 0}, vector<long long>{6, 0, 0, 1, 9, 5, 0, 0, 0}, vector<long long>{0, 9, 8, 0, 0, 0, 0, 6, 0}, vector<long long>{8, 0, 0, 0, 6, 0, 0, 0, 3}, vector<long long>{4, 0, 0, 8, 0, 3, 0, 0, 1}, vector<long long>{7, 0, 0, 0, 2, 0, 0, 0, 6}, vector<long long>{0, 6, 0, 0, 0, 0, 2, 8, 0}, vector<long long>{0, 0, 0, 4, 1, 9, 0, 0, 5}, vector<long long>{0, 0, 0, 0, 8, 0, 0, 7, 9}}) << endl;
    return 0;
}
