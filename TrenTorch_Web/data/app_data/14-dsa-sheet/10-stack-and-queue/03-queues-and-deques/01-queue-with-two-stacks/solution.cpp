#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(1) amortized time per operation, O(n) space
vector<long long> queueWithTwoStacks(vector<string> ops) {
    vector<long long> inbox, outbox, out;
    auto shift = [&]() {
        if (outbox.empty()) {
            while (!inbox.empty()) {
                outbox.push_back(inbox.back());
                inbox.pop_back();
            }
        }
    };
    for (const string& op : ops) {
        if (op.rfind("push", 0) == 0) {
            inbox.push_back(stoll(op.substr(op.find(' ') + 1)));
        } else if (op == "pop") {
            shift();
            out.push_back(outbox.back());
            outbox.pop_back();
        } else if (op == "peek") {
            shift();
            out.push_back(outbox.back());
        } else {
            out.push_back((inbox.empty() && outbox.empty()) ? 1 : 0);
        }
    }
    return out;
}

int main() {
    cout << queueWithTwoStacks(vector<string>{"push 1", "push 2", "peek", "pop", "empty"}) << endl;
    return 0;
}
