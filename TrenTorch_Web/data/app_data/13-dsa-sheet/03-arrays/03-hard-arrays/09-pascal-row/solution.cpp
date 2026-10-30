#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(row) time, O(row) space (entries exceed long long from about row 67 on, so
// this matches the Python output only while the values fit in 64 bits)
vector<long long> pascalRow(long long row) {
    vector<long long> out;
    long long value = 1;
    for (long long i = 0; i <= row; i++) {
        out.push_back(value);
        value = value * (row - i) / (i + 1);
    }
    return out;
}

int main() {
    cout << pascalRow(4) << endl;
    return 0;
}
