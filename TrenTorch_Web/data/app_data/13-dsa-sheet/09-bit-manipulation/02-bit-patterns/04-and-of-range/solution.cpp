#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space
long long andOfRange(long long left, long long right) {
    unsigned long long diff = (unsigned long long)(left ^ right);
    int shift = 0;
    while (diff) {
        shift++;
        diff >>= 1;
    }
    return (left >> shift) << shift;
}

int main() {
    cout << andOfRange(5, 7) << endl;
    return 0;
}
