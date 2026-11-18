#include <bits/stdc++.h>
using namespace std;

// O(n + m) time, O(1) space (fixed 256-entry table)
bool ransomNote(string note, string magazine) {
    int available[256] = {0};
    for (unsigned char c : magazine) available[c]++;
    for (unsigned char c : note) {
        if (--available[c] < 0) return false;
    }
    return true;
}

int main() {
    cout << boolalpha << ransomNote("aab", "baa") << endl;
    return 0;
}
