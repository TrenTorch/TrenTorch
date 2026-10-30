#include <bits/stdc++.h>
using namespace std;

// O(n + m) time (KMP search of goal inside s + s), O(n) space
bool isRotation(string s, string goal) {
    if (s.size() != goal.size()) {
        return false;
    }
    if (goal.empty()) {
        return true;
    }
    // prefix function of goal
    vector<size_t> pi(goal.size(), 0);
    for (size_t i = 1, k = 0; i < goal.size(); i++) {
        while (k > 0 && goal[i] != goal[k]) {
            k = pi[k - 1];
        }
        if (goal[i] == goal[k]) {
            k++;
        }
        pi[i] = k;
    }
    string text = s + s;
    for (size_t i = 0, k = 0; i < text.size(); i++) {
        while (k > 0 && text[i] != goal[k]) {
            k = pi[k - 1];
        }
        if (text[i] == goal[k]) {
            k++;
        }
        if (k == goal.size()) {
            return true;
        }
    }
    return false;
}

int main() {
    cout << boolalpha << isRotation("abcde", "cdeab") << endl;
    return 0;
}
