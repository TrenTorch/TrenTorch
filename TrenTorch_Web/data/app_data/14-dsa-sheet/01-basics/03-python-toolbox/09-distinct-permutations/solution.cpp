#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n * P) time where P = number of distinct permutations, O(n) recursion depth plus output space
vector<string> distinctPermutations(string s) {
    map<char, int> counts;
    for (char c : s) counts[c]++;
    vector<char> letters;
    vector<int> left;
    for (const auto& entry : counts) {
        letters.push_back(entry.first);
        left.push_back(entry.second);
    }
    int n = (int)s.size();
    vector<string> out;
    string prefix;
    function<void()> build = [&]() {
        if ((int)prefix.size() == n) {
            out.push_back(prefix);
            return;
        }
        for (size_t i = 0; i < letters.size(); i++) {
            if (left[i] > 0) {
                left[i]--;
                prefix.push_back(letters[i]);
                build();
                prefix.pop_back();
                left[i]++;
            }
        }
    };
    build();
    return out;
}

int main() {
    cout << distinctPermutations("abc") << endl;
    return 0;
}
