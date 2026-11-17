#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(4^n * n) time, O(n) space (excluding the output)
vector<string> letterCombinations(string digits) {
    const vector<string> keys = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> out;
    if (digits.empty()) return out;
    string prefix;
    function<void(size_t)> go = [&](size_t i) {
        if (i == digits.size()) {
            out.push_back(prefix);
            return;
        }
        for (char letter : keys[digits[i] - '0']) {
            prefix.push_back(letter);
            go(i + 1);
            prefix.pop_back();
        }
    };
    go(0);
    return out;
}

int main() {
    cout << letterCombinations("23") << endl;
    return 0;
}
