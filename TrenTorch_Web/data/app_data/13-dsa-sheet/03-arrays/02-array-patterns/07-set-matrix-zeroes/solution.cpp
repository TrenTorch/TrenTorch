#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R+C) space
vector<vector<long long>> setMatrixZeroes(vector<vector<long long>> matrix) {
    int R = matrix.size();
    if (R == 0) return {};
    int C = matrix[0].size();
    vector<bool> rowZero(R, false), colZero(C, false);
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++) {
            if (matrix[i][j] == 0) {
                rowZero[i] = true;
                colZero[j] = true;
            }
        }
    }
    vector<vector<long long>> out(R, vector<long long>(C));
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++) {
            out[i][j] = (rowZero[i] || colZero[j]) ? 0 : matrix[i][j];
        }
    }
    return out;
}

int main() {
    cout << setMatrixZeroes(vector<vector<long long>>{vector<long long>{1, 2, 3}, vector<long long>{4, 0, 6}, vector<long long>{7, 8, 9}}) << endl;
    return 0;
}
