#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(rows * cols) time, O(rows * cols) space for the result
vector<vector<long long>> transposeMatrix(vector<vector<long long>> matrix) {
    if (matrix.empty() || matrix[0].empty()) return {};
    size_t rows = matrix.size();
    size_t cols = matrix[0].size();
    vector<vector<long long>> out(cols, vector<long long>(rows, 0));
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            out[j][i] = matrix[i][j];
        }
    }
    return out;
}

int main() {
    cout << transposeMatrix(vector<vector<long long>>{vector<long long>{1, 2, 3}, vector<long long>{4, 5, 6}}) << endl;
    return 0;
}
