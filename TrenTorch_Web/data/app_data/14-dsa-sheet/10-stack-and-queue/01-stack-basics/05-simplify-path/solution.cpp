#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
string simplifyPath(string path) {
    vector<string> stk;
    stringstream ss(path);
    string name;
    while (getline(ss, name, '/')) {
        if (name == "..") {
            if (!stk.empty()) stk.pop_back();
        } else if (!name.empty() && name != ".") {
            stk.push_back(name);
        }
    }
    string result = "/";
    for (size_t i = 0; i < stk.size(); i++) {
        if (i) result += "/";
        result += stk[i];
    }
    return result;
}

int main() {
    cout << simplifyPath("/home/") << endl;
    return 0;
}
