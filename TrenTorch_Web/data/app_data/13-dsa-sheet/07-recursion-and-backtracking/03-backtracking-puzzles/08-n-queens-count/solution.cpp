#include <bits/stdc++.h>
using namespace std;

// O(n!) time worst case with set lookups, O(n) space
long long nQueensCount(long long n) {
    set<long long> cols, diag1, diag2;
    function<long long(long long)> go = [&](long long r) -> long long {
        if (r == n) return 1;
        long long total = 0;
        for (long long c = 0; c < n; c++) {
            if (cols.count(c) || diag1.count(r - c) || diag2.count(r + c)) continue;
            cols.insert(c);
            diag1.insert(r - c);
            diag2.insert(r + c);
            total += go(r + 1);
            cols.erase(c);
            diag1.erase(r - c);
            diag2.erase(r + c);
        }
        return total;
    };
    return go(0);
}

int main() {
    cout << nQueensCount(4) << endl;
    return 0;
}
