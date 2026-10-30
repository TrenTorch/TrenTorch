#include <bits/stdc++.h>
using namespace std;

// O(output length) time, O(output length) space
string decodeString(string s) {
    string out;
    vector<pair<size_t, long long>> blocks;
    long long num = 0;
    for (char ch : s) {
        if (isdigit((unsigned char)ch)) {
            num = num * 10 + (ch - '0');
        } else if (ch == '[') {
            blocks.push_back({out.size(), num});
            num = 0;
        } else if (ch == ']') {
            size_t start = blocks.back().first;
            long long count = blocks.back().second;
            blocks.pop_back();
            if (count == 0) {
                out.erase(start);
            } else if (count > 1) {
                string block = out.substr(start);
                for (long long k = 1; k < count; k++) out += block;
            }
        } else {
            out.push_back(ch);
        }
    }
    return out;
}

int main() {
    cout << decodeString("3[a2[c]]") << endl;
    return 0;
}
