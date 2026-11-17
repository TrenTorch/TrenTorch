#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(4^n / sqrt(n)) time (number of valid strings times length), O(n) recursion depth
vector<string> generateParentheses(long long n) {
    vector<string> out;
    function<void(string, long long, long long)> go = [&](string prefix, long long opens, long long closes) {
        if ((long long)prefix.size() == 2 * n) {
            out.push_back(prefix);
            return;
        }
        if (opens < n) go(prefix + "(", opens + 1, closes);
        if (closes < opens) go(prefix + ")", opens, closes + 1);
    };
    go("", 0, 0);
    return out;
}

int main() {
    cout << generateParentheses(3) << endl;
    return 0;
}
