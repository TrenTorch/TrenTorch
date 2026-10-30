#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(R*C) time, O(R*C) space for the output
vector<long long> spiralOrder(vector<vector<long long>> matrix) {
    if (matrix.empty() || matrix[0].empty()) return {};
    vector<long long> out;
    int top = 0, bottom = matrix.size() - 1;
    int left = 0, right = matrix[0].size() - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) out.push_back(matrix[top][j]);
        for (int i = top + 1; i <= bottom; i++) out.push_back(matrix[i][right]);
        if (top < bottom) {
            for (int j = right - 1; j >= left; j--) out.push_back(matrix[bottom][j]);
        }
        if (left < right) {
            for (int i = bottom - 1; i > top; i--) out.push_back(matrix[i][left]);
        }
        top++;
        bottom--;
        left++;
        right--;
    }
    return out;
}

int main() {
    cout << spiralOrder(vector<vector<long long>>{vector<long long>{1, 2, 3}, vector<long long>{4, 5, 6}, vector<long long>{7, 8, 9}}) << endl;
    return 0;
}
