#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

void allCombinationsGo(long long n, long long k, long long start, vector<long long>& current,
                       vector<vector<long long>>& out) {
    long long need = k - (long long)current.size();
    if (need == 0) {
        out.push_back(current);
        return;
    }
    for (long long j = start; j < n - need + 2; j++) {
        current.push_back(j);
        allCombinationsGo(n, k, j + 1, current, out);
        current.pop_back();
    }
}

// O(C(n,k) * k) time, O(k) recursion space plus the output
vector<vector<long long>> allCombinations(long long n, long long k) {
    vector<vector<long long>> out;
    vector<long long> current;
    allCombinationsGo(n, k, 1, current, out);
    return out;
}

int main() {
    cout << allCombinations(4, 2) << endl;
    return 0;
}
