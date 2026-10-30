#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void hanoiMove(long long k, long long source, long long target, long long spare,
               vector<vector<long long>>& moves) {
    if (k == 0) return;
    hanoiMove(k - 1, source, spare, target, moves);
    moves.push_back({source, target});
    hanoiMove(k - 1, spare, target, source, moves);
}

// O(2^n) time, O(2^n) space for the moves (O(n) recursion depth)
vector<vector<long long>> towerOfHanoi(long long n) {
    vector<vector<long long>> moves;
    hanoiMove(n, 1, 3, 2, moves);
    return moves;
}

int main() {
    cout << towerOfHanoi(2) << endl;
    return 0;
}
