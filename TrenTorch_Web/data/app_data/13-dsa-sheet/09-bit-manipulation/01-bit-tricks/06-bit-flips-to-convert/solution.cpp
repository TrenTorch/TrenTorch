#include <bits/stdc++.h>
using namespace std;

// O(k) time where k is the number of differing bits, O(1) space
long long bitFlipsToConvert(long long a, long long b) {
    long long diff = a ^ b;
    long long count = 0;
    while (diff) {
        diff &= diff - 1;
        count++;
    }
    return count;
}

int main() {
    cout << bitFlipsToConvert(10, 7) << endl;
    return 0;
}
