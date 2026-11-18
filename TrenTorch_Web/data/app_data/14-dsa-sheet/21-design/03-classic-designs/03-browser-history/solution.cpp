#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(k) time per back/forward with k <= 100 steps, O(m) space for m visits
vector<string> runBrowserHistory(string homepage, vector<string> ops) {
    vector<string> history{homepage};
    long long index = 0;
    vector<string> out;
    for (const string& op : ops) {
        istringstream iss(op);
        string kind, arg;
        iss >> kind >> arg;
        if (kind == "visit") {
            history.resize(static_cast<size_t>(index + 1));
            history.push_back(arg);
            index++;
        } else if (kind == "back") {
            index = max(0LL, index - stoll(arg));
            out.push_back(history[index]);
        } else {
            index = min((long long)history.size() - 1, index + stoll(arg));
            out.push_back(history[index]);
        }
    }
    return out;
}

int main() {
    cout << runBrowserHistory("a", vector<string>{"visit b", "visit c", "back 1", "back 5", "forward 1", "visit d", "forward 3"}) << endl;
    return 0;
}
