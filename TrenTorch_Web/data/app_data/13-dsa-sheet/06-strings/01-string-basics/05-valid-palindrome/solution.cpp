#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) space
bool validPalindrome(string s) {
    long long i = 0, j = (long long)s.size() - 1;
    while (i < j) {
        if (!isalnum((unsigned char)s[i])) {
            i++;
        } else if (!isalnum((unsigned char)s[j])) {
            j--;
        } else {
            if (tolower((unsigned char)s[i]) != tolower((unsigned char)s[j])) {
                return false;
            }
            i++;
            j--;
        }
    }
    return true;
}

int main() {
    cout << boolalpha << validPalindrome("A man, a plan, a canal: Panama") << endl;
    return 0;
}
