#include <bits/stdc++.h>
using namespace std;

// O(log n) time, O(1) space (plus O(log n) digits for the final number)
long long nthDigit(long long n) {
    long long length = 1, count = 9, start = 1;
    while (n > length * count) {
        n -= length * count;
        length++;
        count *= 10;
        start *= 10;
    }
    long long number = start + (n - 1) / length;
    string s = to_string(number);
    return s[(n - 1) % length] - '0';
}

int main() {
    cout << nthDigit(11) << endl;
    return 0;
}
