#include <bits/stdc++.h>
using namespace std;

// O((k + 1) * m) time, O(n) space (m = number of flights)
long long cheapestPrice(long long n, vector<vector<long long>> flights, long long src, long long dst, long long k) {
    const long long INF = LLONG_MAX / 4;
    vector<long long> best(n, INF);
    best[src] = 0;
    for (long long round = 0; round < k + 1; round++) {
        vector<long long> nxt = best;
        for (const auto& f : flights) {
            long long a = f[0];
            long long b = f[1];
            long long price = f[2];
            if (best[a] < INF && best[a] + price < nxt[b]) nxt[b] = best[a] + price;
        }
        best = nxt;
    }
    return best[dst] < INF ? best[dst] : -1;
}

int main() {
    cout << cheapestPrice(4, vector<vector<long long>>{vector<long long>{0, 1, 100}, vector<long long>{1, 2, 100}, vector<long long>{2, 0, 100}, vector<long long>{1, 3, 600}, vector<long long>{2, 3, 200}}, 0, 3, 1) << endl;
    return 0;
}
