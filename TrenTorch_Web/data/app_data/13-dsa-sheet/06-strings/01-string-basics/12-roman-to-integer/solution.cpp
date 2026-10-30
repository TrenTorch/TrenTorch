#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
long long romanToInteger(string s) {
    auto value = [](char c) -> long long {
        switch (c) {
            case 'I': return 1;
            case 'V': return 5;
            case 'X': return 10;
            case 'L': return 50;
            case 'C': return 100;
            case 'D': return 500;
            case 'M': return 1000;
        }
        return 0;
    };
    long long total = 0;
    for (size_t i = 0; i < s.size(); i++) {
        if (i + 1 < s.size() && value(s[i]) < value(s[i + 1])) {
            total -= value(s[i]);
        } else {
            total += value(s[i]);
        }
    }
    return total;
}

int main() {
    cout << romanToInteger("III") << endl;
    return 0;
}
