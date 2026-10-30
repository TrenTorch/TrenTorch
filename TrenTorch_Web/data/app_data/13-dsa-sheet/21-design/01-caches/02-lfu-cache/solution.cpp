#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(1) time per operation, O(capacity) space
vector<long long> runLfu(long long capacity, vector<string> ops) {
    vector<long long> out;
    unordered_map<long long, long long> value, count;
    map<long long, list<long long>> groups;  // frequency -> keys, least recent at front
    unordered_map<long long, list<long long>::iterator> where;
    long long low = 0;
    auto touch = [&](long long key) {
        long long c = count[key];
        groups[c].erase(where[key]);
        if (groups[c].empty()) {
            groups.erase(c);
            if (low == c) low++;
        }
        count[key] = c + 1;
        groups[c + 1].push_back(key);
        where[key] = prev(groups[c + 1].end());
    };
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        long long key;
        iss >> kind >> key;
        if (kind == "get") {
            if (value.count(key)) {
                touch(key);
                out.push_back(value[key]);
            } else {
                out.push_back(-1);
            }
        } else if (capacity > 0) {
            long long v;
            iss >> v;
            if (value.count(key)) {
                value[key] = v;
                touch(key);
            } else {
                if ((long long)value.size() == capacity) {
                    long long oldest = groups[low].front();
                    groups[low].pop_front();
                    if (groups[low].empty()) groups.erase(low);
                    value.erase(oldest);
                    count.erase(oldest);
                    where.erase(oldest);
                }
                value[key] = v;
                count[key] = 1;
                groups[1].push_back(key);
                where[key] = prev(groups[1].end());
                low = 1;
            }
        }
    }
    return out;
}

int main() {
    cout << runLfu(2, vector<string>{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "get 3", "put 4 4", "get 1", "get 3", "get 4"}) << endl;
    return 0;
}
