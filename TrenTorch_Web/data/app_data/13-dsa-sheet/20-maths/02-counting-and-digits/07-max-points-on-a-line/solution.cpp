#include <bits/stdc++.h>
using namespace std;

// O(n^2 log C) time, O(n) space
long long maxPoints(vector<vector<long long>> points) {
    long long n = points.size();
    if (n <= 2) return n;
    long long best = 2;
    for (long long i = 0; i < n; i++) {
        map<pair<long long, long long>, long long> slopes;
        long long x0 = points[i][0], y0 = points[i][1];
        for (long long j = i + 1; j < n; j++) {
            long long dx = points[j][0] - x0, dy = points[j][1] - y0;
            long long g = std::gcd(dx, dy);
            dx /= g;
            dy /= g;
            if (dx < 0 || (dx == 0 && dy < 0)) {
                dx = -dx;
                dy = -dy;
            }
            slopes[{dx, dy}]++;
        }
        if (!slopes.empty()) {
            long long mx = 0;
            for (auto& kv : slopes) mx = max(mx, kv.second);
            best = max(best, mx + 1);
        }
    }
    return best;
}

int main() {
    cout << maxPoints(vector<vector<long long>>{vector<long long>{1, 1}, vector<long long>{2, 2}, vector<long long>{3, 3}}) << endl;
    return 0;
}
