#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space
long long countTripleLoop(long long n) {
    return n * (n + 1) * (n + 2) / 6;
}

int main() {
    cout << countTripleLoop(3) << endl;
    return 0;
}
