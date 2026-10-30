#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R*C) space for the output
vector<vector<long long>> rotateMatrix(vector<vector<long long>> matrix) {
    int R = matrix.size();
    if (R == 0 || matrix[0].empty()) return {};
    int C = matrix[0].size();
    vector<vector<long long>> out(C, vector<long long>(R));
    for (int j = 0; j < C; j++) {
        for (int i = 0; i < R; i++) {
            out[j][i] = matrix[R - 1 - i][j];
        }
    }
    return out;
}

int main() {
    cout << rotateMatrix(vector<vector<long long>>{vector<long long>{1, 2, 3}, vector<long long>{4, 5, 6}}) << endl;
    return 0;
}
