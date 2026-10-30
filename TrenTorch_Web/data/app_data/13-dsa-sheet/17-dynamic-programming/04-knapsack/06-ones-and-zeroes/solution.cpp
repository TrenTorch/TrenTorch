#include <bits/stdc++.h>
using namespace std;

// O(len(strs) * m * n) time, O(m * n) space
long long findMaxForm(vector<string> strs, long long m, long long n) {
    int M = m, N = n;
    vector<vector<long long>> best(M + 1, vector<long long>(N + 1, 0));
    for (const string& s : strs) {
        int zeros = count(s.begin(), s.end(), '0');
        int ones = (int)s.size() - zeros;
        for (int z = M; z >= zeros; --z) {
            vector<long long>& row = best[z];
            vector<long long>& source = best[z - zeros];
            for (int o = N; o >= ones; --o) {
                if (source[o - ones] + 1 > row[o]) row[o] = source[o - ones] + 1;
            }
        }
    }
    return best[M][N];
}

int main() {
    cout << findMaxForm(vector<string>{"10", "0001", "111001", "1", "0"}, 5, 3) << endl;
    return 0;
}
