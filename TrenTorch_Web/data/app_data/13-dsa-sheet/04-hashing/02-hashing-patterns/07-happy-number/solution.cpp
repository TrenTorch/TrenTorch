#include <bits/stdc++.h>
using namespace std;

long long sumOfDigitSquares(long long x) {
    long long total = 0;
    while (x) {
        long long digit = x % 10;
        total += digit * digit;
        x /= 10;
    }
    return total;
}

// O(log n) time, O(1) space
bool happyNumber(long long n) {
    long long slow = n;
    long long fast = sumOfDigitSquares(n);
    while (fast != 1 && slow != fast) {
        slow = sumOfDigitSquares(slow);
        fast = sumOfDigitSquares(sumOfDigitSquares(fast));
    }
    return fast == 1;
}

int main() {
    cout << boolalpha << happyNumber(19) << endl;
    return 0;
}
