#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string removeKDigits(string num, long long k) {
    string stack;
    for (char ch : num) {
        while (k && !stack.empty() && stack.back() > ch) {
            stack.pop_back();
            k--;
        }
        stack.push_back(ch);
    }
    if (k) stack.resize(stack.size() > (size_t)k ? stack.size() - k : 0);
    size_t p = stack.find_first_not_of('0');
    if (p == string::npos) return "0";
    return stack.substr(p);
}

int main() {
    cout << removeKDigits("1432219", 3) << endl;
    return 0;
}
