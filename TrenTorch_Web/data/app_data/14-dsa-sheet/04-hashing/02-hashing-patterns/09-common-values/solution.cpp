#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O((n + m) log(n + m)) time, O(n + m) space
vector<long long> commonValues(vector<long long> a, vector<long long> b) {
    set<long long> setA(a.begin(), a.end());
    set<long long> setB(b.begin(), b.end());
    vector<long long> result;
    for (long long x : setA) {
        if (setB.count(x)) result.push_back(x);
    }
    return result;
}

int main() {
    cout << commonValues(vector<long long>{1, 2, 2, 3}, vector<long long>{2, 2, 3, 4}) << endl;
    return 0;
}
