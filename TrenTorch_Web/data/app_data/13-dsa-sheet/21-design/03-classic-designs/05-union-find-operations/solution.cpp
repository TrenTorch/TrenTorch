#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// Near O(1) amortized time per operation (union by size, path halving), O(n) space
vector<long long> runUnionFind(long long n, vector<string> ops) {
    vector<long long> parent(n), sz(n, 1);
    iota(parent.begin(), parent.end(), 0LL);
    auto findRoot = [&](long long x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    };
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        long long a, b;
        iss >> kind;
        if (kind == "union") {
            iss >> a >> b;
            a = findRoot(a);
            b = findRoot(b);
            if (a != b) {
                if (sz[a] < sz[b]) swap(a, b);
                parent[b] = a;
                sz[a] += sz[b];
            }
        } else if (kind == "connected") {
            iss >> a >> b;
            out.push_back(findRoot(a) == findRoot(b) ? 1 : 0);
        } else {
            iss >> a;
            out.push_back(sz[findRoot(a)]);
        }
    }
    return out;
}

int main() {
    cout << runUnionFind(5, vector<string>{"union 0 1", "union 1 2", "connected 0 2", "connected 0 3", "size 2"}) << endl;
    return 0;
}
