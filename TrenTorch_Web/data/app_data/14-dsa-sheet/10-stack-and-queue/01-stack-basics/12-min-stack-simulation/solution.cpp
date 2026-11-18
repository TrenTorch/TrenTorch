#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> minStack(vector<string> ops) {
    vector<long long> values, mins, out;
    for (const string& op : ops) {
        if (op.rfind("push", 0) == 0) {
            long long x = stoll(op.substr(op.find(' ') + 1));
            values.push_back(x);
            mins.push_back(mins.empty() ? x : min(x, mins.back()));
        } else if (op == "pop") {
            values.pop_back();
            mins.pop_back();
        } else if (op == "top") {
            out.push_back(values.back());
        } else {
            out.push_back(mins.back());
        }
    }
    return out;
}

int main() {
    cout << minStack(vector<string>{"push 5", "push 3", "get_min", "pop", "top", "get_min"}) << endl;
    return 0;
}
