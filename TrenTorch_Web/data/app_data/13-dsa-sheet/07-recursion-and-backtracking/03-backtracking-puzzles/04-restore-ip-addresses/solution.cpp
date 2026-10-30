#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(1) time for fixed-size search (at most 3^4 splits), O(1) extra space besides the output
vector<string> restoreIpAddresses(string s) {
    vector<string> out;
    auto valid = [](const string& part) -> bool {
        if (part.size() > 1 && part[0] == '0') return false;
        return stoi(part) <= 255;
    };
    vector<string> parts;
    function<void(size_t)> go = [&](size_t start) {
        if (parts.size() == 4) {
            if (start == s.size()) {
                string joined;
                for (size_t i = 0; i < parts.size(); i++) {
                    if (i) joined += '.';
                    joined += parts[i];
                }
                out.push_back(joined);
            }
            return;
        }
        for (size_t length = 1; length <= 3; length++) {
            if (start + length > s.size()) break;
            string part = s.substr(start, length);
            if (valid(part)) {
                parts.push_back(part);
                go(start + length);
                parts.pop_back();
            }
        }
    };
    go(0);
    sort(out.begin(), out.end());
    return out;
}

int main() {
    cout << restoreIpAddresses("25525511135") << endl;
    return 0;
}
