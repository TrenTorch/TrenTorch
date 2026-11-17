#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n * bits) space
vector<string> binaryNumbersUpTo(long long n) {
    vector<string> out;
    deque<string> queue;
    queue.push_back("1");
    for (long long t = 0; t < n; t++) {
        string front = queue.front();
        queue.pop_front();
        out.push_back(front);
        queue.push_back(front + "0");
        queue.push_back(front + "1");
    }
    return out;
}

int main() {
    cout << binaryNumbersUpTo(5) << endl;
    return 0;
}
