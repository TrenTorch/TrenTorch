#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n^3) time, O(n^2) space
vector<vector<long long>> allPairsShortest(long long n, vector<vector<long long>> edges) {
    const long long INF = LLONG_MAX / 4;
    int N = n;
    vector<vector<long long>> dist(N, vector<long long>(N, INF));
    for (int i = 0; i < N; i++) dist[i][i] = 0;
    for (auto& e : edges) {
        int a = e[0], b = e[1];
        long long w = e[2];
        if (w < dist[a][b]) dist[a][b] = w;
    }
    for (int k = 0; k < N; k++) {
        vector<long long>& row_k = dist[k];
        for (int i = 0; i < N; i++) {
            long long dik = dist[i][k];
            if (dik == INF) continue;
            vector<long long>& row_i = dist[i];
            for (int j = 0; j < N; j++) {
                if (dik + row_k[j] < row_i[j]) row_i[j] = dik + row_k[j];
            }
        }
    }
    for (auto& row : dist)
        for (auto& x : row)
            if (x >= INF) x = -1;
    return dist;
}

int main() {
    cout << allPairsShortest(3, vector<vector<long long>>{vector<long long>{0, 1, 4}, vector<long long>{1, 2, 1}, vector<long long>{0, 2, 7}}) << endl;
    return 0;
}
