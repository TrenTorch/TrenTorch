#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(1) amortized time per operation, O(window) space
vector<long long> runHitCounter(vector<string> ops) {
    deque<long long> window;
    vector<long long> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind;
        long long t;
        iss >> kind >> t;
        if (kind == "hit") {
            window.push_back(t);
        } else {
            while (!window.empty() && window.front() <= t - 300) window.pop_front();
            out.push_back((long long)window.size());
        }
    }
    return out;
}

int main() {
    cout << runHitCounter(vector<string>{"hit 1", "hit 2", "hit 3", "count 4", "hit 300", "count 300", "count 301"}) << endl;
    return 0;
}
