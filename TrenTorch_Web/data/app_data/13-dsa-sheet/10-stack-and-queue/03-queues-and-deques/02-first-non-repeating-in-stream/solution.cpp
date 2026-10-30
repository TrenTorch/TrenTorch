#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(1) extra space (alphabet-sized counts)
string firstNonRepeatingStream(string s) {
    vector<int> counts(256, 0);
    deque<char> queue;
    string out;
    for (char ch : s) {
        unsigned char u = (unsigned char)ch;
        counts[u]++;
        if (counts[u] == 1) queue.push_back(ch);
        while (!queue.empty() && counts[(unsigned char)queue.front()] > 1) queue.pop_front();
        out.push_back(queue.empty() ? '#' : queue.front());
    }
    return out;
}

int main() {
    cout << firstNonRepeatingStream("aabc") << endl;
    return 0;
}
