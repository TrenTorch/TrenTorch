#include <bits/stdc++.h>
using namespace std;

// O(1) time, O(1) space (fixed number of denominations)
long long fewestNotes(long long amount) {
    const long long values[] = {2000, 500, 100, 50, 20, 10, 5, 2, 1};
    long long total = 0;
    for (long long value : values) {
        total += amount / value;
        amount %= value;
    }
    return total;
}

int main() {
    cout << fewestNotes(70) << endl;
    return 0;
}
