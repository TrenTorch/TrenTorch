#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
bool lemonadeChange(vector<long long> bills) {
    long long fives = 0, tens = 0;
    for (long long bill : bills) {
        if (bill == 5) {
            fives++;
        } else if (bill == 10) {
            if (fives == 0) return false;
            fives--;
            tens++;
        } else {
            if (tens > 0 && fives > 0) {
                tens--;
                fives--;
            } else if (fives >= 3) {
                fives -= 3;
            } else {
                return false;
            }
        }
    }
    return true;
}

int main() {
    cout << boolalpha << lemonadeChange(vector<long long>{5, 5, 5, 10, 20}) << endl;
    return 0;
}
