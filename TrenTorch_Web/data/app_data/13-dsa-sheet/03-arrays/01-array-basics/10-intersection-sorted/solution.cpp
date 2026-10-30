#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n + m) time, O(min(n, m)) space for the output
vector<long long> intersectionSorted(vector<long long> a, vector<long long> b) {
    vector<long long> out;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] == b[j]) {
            out.push_back(a[i]);
            i++;
            j++;
        } else if (a[i] < b[j]) {
            i++;
        } else {
            j++;
        }
    }
    return out;
}

int main() {
    cout << intersectionSorted(vector<long long>{1, 2, 2, 3}, vector<long long>{2, 2, 2, 4}) << endl;
    return 0;
}
