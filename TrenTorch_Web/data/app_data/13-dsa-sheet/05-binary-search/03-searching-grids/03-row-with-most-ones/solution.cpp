#include <bits/stdc++.h>
using namespace std;

// O(rows + cols) time, O(1) space
long long rowWithMostOnes(vector<vector<long long>> matrix) {
    long long bestRow = -1;
    long long col = matrix.empty() ? 0 : (long long)matrix[0].size();
    for (long long i = 0; i < (long long)matrix.size(); i++) {
        bool moved = false;
        while (col > 0 && matrix[i][col - 1] == 1) {
            col--;
            moved = true;
        }
        if (moved) {
            bestRow = i;
        }
    }
    return bestRow;
}

int main() {
    cout << rowWithMostOnes(vector<vector<long long>>{vector<long long>{0, 0, 1, 1}, vector<long long>{0, 1, 1, 1}, vector<long long>{0, 0, 0, 1}}) << endl;
    return 0;
}
