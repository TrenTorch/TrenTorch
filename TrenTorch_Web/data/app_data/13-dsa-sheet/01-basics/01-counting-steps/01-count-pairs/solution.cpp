#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long countPairs(long long n) {
    return n * (n - 1) / 2;
}

int main() {
    cout << countPairs(4) << endl;
    return 0;
}
