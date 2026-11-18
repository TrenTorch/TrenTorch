#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(1) time per operation, O(capacity) space
vector<long long> runLru(long long capacity, vector<string> ops) {
    vector<long long> out;
    list<pair<long long, long long>> order;  // front = most recently used
    unordered_map<long long, list<pair<long long, long long>>::iterator> pos;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        iss >> kind;
        if (kind == "get") {
            long long key;
            iss >> key;
            auto it = pos.find(key);
            if (it != pos.end()) {
                order.splice(order.begin(), order, it->second);
                out.push_back(it->second->second);
            } else {
                out.push_back(-1);
            }
        } else if (capacity > 0) {
            long long key, value;
            iss >> key >> value;
            auto it = pos.find(key);
            if (it != pos.end()) {
                it->second->second = value;
                order.splice(order.begin(), order, it->second);
            } else {
                if ((long long)order.size() == capacity) {
                    pos.erase(order.back().first);
                    order.pop_back();
                }
                order.push_front({key, value});
                pos[key] = order.begin();
            }
        }
    }
    return out;
}

int main() {
    cout << runLru(2, vector<string>{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "put 4 4", "get 1", "get 3", "get 4"}) << endl;
    return 0;
}
