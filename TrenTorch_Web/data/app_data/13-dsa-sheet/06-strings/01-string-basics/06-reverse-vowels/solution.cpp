#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) extra space (s is modified in place and returned)
string reverseVowels(string s) {
    auto isVowel = [](char c) {
        char l = (char)tolower((unsigned char)c);
        return l == 'a' || l == 'e' || l == 'i' || l == 'o' || l == 'u';
    };
    long long i = 0, j = (long long)s.size() - 1;
    while (i < j) {
        while (i < j && !isVowel(s[i])) {
            i++;
        }
        while (i < j && !isVowel(s[j])) {
            j--;
        }
        if (i < j) {
            swap(s[i], s[j]);
            i++;
            j--;
        }
    }
    return s;
}

int main() {
    cout << reverseVowels("hello") << endl;
    return 0;
}
