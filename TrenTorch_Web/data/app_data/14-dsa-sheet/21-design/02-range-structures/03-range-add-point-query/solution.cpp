#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log n) time per operation, O(n) space
vector<long long> runRangeAdd(long long n, vector<string> ops) {
    vector<long long> tree(n + 2, 0);
    auto add = [&](long long i, long long delta) {
        for (i++; i <= n + 1; i += i & -i) tree[i] += delta;
    };
    auto prefix = [&](long long i) {
        long long total = 0;
        for (i++; i > 0; i -= i & -i) total += tree[i];
        return total;
    };
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        iss >> kind;
        if (kind == "add") {
            long long left, right, v;
            iss >> left >> right >> v;
            add(left, v);
            add(right + 1, -v);
        } else {
            long long i;
            iss >> i;
            out.push_back(prefix(i));
        }
    }
    return out;
}

int main() {
    cout << runRangeAdd(5, vector<string>{"add 1 3 10", "get 2", "add 0 4 -1", "get 0", "get 3"}) << endl;
    return 0;
}
