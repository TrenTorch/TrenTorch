#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(F(n) * n) time where F(n) is the number of answers (about 1.6^n), O(n) recursion depth
vector<string> noAdjacentOnes(long long n) {
    vector<string> out;
    function<void(string)> go = [&](string prefix) {
        if ((long long)prefix.size() == n) {
            out.push_back(prefix);
            return;
        }
        go(prefix + "0");
        if (prefix.empty() || prefix.back() != '1') go(prefix + "1");
    };
    go("");
    return out;
}

int main() {
    cout << noAdjacentOnes(3) << endl;
    return 0;
}
