#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string zigzagConversion(string s, long long rows) {
    if (rows == 1 || rows >= (long long)s.size()) return s;
    vector<string> lines(rows);
    long long row = 0, step = 1;
    for (char ch : s) {
        lines[row] += ch;
        if (row == 0) {
            step = 1;
        } else if (row == rows - 1) {
            step = -1;
        }
        row += step;
    }
    string out;
    for (const string& line : lines) out += line;
    return out;
}

int main() {
    cout << zigzagConversion("PAYPALISHIRING", 3) << endl;
    return 0;
}
