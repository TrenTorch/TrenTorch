#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(log n) time per get (n = values stored for that key), O(m) space for m sets
vector<string> runTimeMap(vector<string> ops) {
    unordered_map<string, vector<long long>> times;
    unordered_map<string, vector<string>> values;
    vector<string> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind, key;
        iss >> kind >> key;
        if (kind == "set") {
            string value;
            long long t;
            iss >> value >> t;
            times[key].push_back(t);
            values[key].push_back(value);
        } else {
            long long t;
            iss >> t;
            size_t i = 0;
            auto it = times.find(key);
            if (it != times.end()) {
                i = upper_bound(it->second.begin(), it->second.end(), t) - it->second.begin();
            }
            out.push_back(i ? values[key][i - 1] : string());
        }
    }
    return out;
}

int main() {
    cout << runTimeMap(vector<string>{"set love high 10", "get love 10", "get love 15", "set love low 20", "get love 15", "get love 25", "get love 5"}) << endl;
    return 0;
}
