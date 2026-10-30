#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log s) time per get (s = changes to that index), O(m) space for m sets
vector<long long> runSnapshotArray(long long length, vector<string> ops) {
    unordered_map<long long, vector<long long>> ids, vals;
    long long snapId = 0;
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        iss >> kind;
        if (kind == "set") {
            long long i, v;
            iss >> i >> v;
            vector<long long>& idv = ids[i];
            vector<long long>& vv = vals[i];
            if (!idv.empty() && idv.back() == snapId) {
                vv.back() = v;
            } else {
                idv.push_back(snapId);
                vv.push_back(v);
            }
        } else if (kind == "snap") {
            out.push_back(snapId);
            snapId++;
        } else {
            long long i, want;
            iss >> i >> want;
            long long val = 0;
            auto it = ids.find(i);
            if (it != ids.end()) {
                const vector<long long>& idv = it->second;
                long long k = (long long)(upper_bound(idv.begin(), idv.end(), want) - idv.begin()) - 1;
                if (k >= 0) val = vals[i][k];
            }
            out.push_back(val);
        }
    }
    return out;
}

int main() {
    cout << runSnapshotArray(3, vector<string>{"set 0 5", "snap", "set 0 6", "get 0 0", "snap", "get 0 1"}) << endl;
    return 0;
}
