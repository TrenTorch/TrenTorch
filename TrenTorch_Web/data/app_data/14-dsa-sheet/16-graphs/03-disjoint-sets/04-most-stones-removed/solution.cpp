#include <bits/stdc++.h>
using namespace std;

// O(S log S) time, O(S) space (S = number of stones; ordered maps used for the sparse DSU)
long long removeStones(vector<vector<long long>> stones) {
    map<long long, long long> parent, sz;
    auto findRoot = [&](long long a) -> long long {
        if (!parent.count(a)) {
            parent[a] = a;
            sz[a] = 1;
        }
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    };
    for (auto& s : stones) {
        long long ra = findRoot(s[0]);
        long long rb = findRoot(s[1] + 10001);
        if (ra != rb) {
            if (sz[ra] < sz[rb]) swap(ra, rb);
            parent[rb] = ra;
            sz[ra] += sz[rb];
        }
    }
    set<long long> groups;
    for (auto& s : stones) groups.insert(findRoot(s[0]));
    return (long long)stones.size() - (long long)groups.size();
}

int main() {
    cout << removeStones(vector<vector<long long>>{vector<long long>{0, 0}, vector<long long>{0, 1}, vector<long long>{1, 0}, vector<long long>{1, 2}, vector<long long>{2, 1}, vector<long long>{2, 2}}) << endl;
    return 0;
}
