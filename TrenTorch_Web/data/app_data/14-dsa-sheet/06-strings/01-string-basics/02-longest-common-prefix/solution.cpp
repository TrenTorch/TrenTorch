#include <bits/stdc++.h>
using namespace std;

// O(n * L) time for n words of max length L, O(1) extra space
string longestCommonPrefix(vector<string> words) {
    if (words.empty()) {
        return "";
    }
    string first = *min_element(words.begin(), words.end());
    string last = *max_element(words.begin(), words.end());
    size_t i = 0;
    while (i < first.size() && i < last.size() && first[i] == last[i]) {
        i++;
    }
    return first.substr(0, i);
}

int main() {
    cout << longestCommonPrefix(vector<string>{"flower", "flow", "flight"}) << endl;
    return 0;
}
