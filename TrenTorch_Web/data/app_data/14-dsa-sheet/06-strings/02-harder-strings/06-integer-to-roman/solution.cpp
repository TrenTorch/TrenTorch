#include <bits/stdc++.h>
using namespace std;

// O(1) time (fixed 13-entry table), O(1) space
string integerToRoman(long long num) {
    vector<pair<long long, string>> table = {
        {1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"}, {90, "XC"},
        {50, "L"}, {40, "XL"}, {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};
    string out;
    for (const auto& entry : table) {
        long long count = num / entry.first;
        num %= entry.first;
        for (long long k = 0; k < count; k++) out += entry.second;
    }
    return out;
}

int main() {
    cout << integerToRoman(3) << endl;
    return 0;
}
