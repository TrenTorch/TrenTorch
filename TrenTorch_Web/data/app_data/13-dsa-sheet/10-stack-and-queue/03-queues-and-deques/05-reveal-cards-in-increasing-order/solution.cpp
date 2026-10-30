#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n log n) time (sorting), O(n) space
vector<long long> revealCards(vector<long long> deck) {
    int n = deck.size();
    vector<long long> result(n, 0);
    deque<int> positions;
    for (int i = 0; i < n; i++) positions.push_back(i);
    vector<long long> sortedDeck = deck;
    sort(sortedDeck.begin(), sortedDeck.end());
    for (long long card : sortedDeck) {
        result[positions.front()] = card;
        positions.pop_front();
        if (!positions.empty()) {
            positions.push_back(positions.front());
            positions.pop_front();
        }
    }
    return result;
}

int main() {
    cout << revealCards(vector<long long>{17, 13, 11, 2, 3, 5, 7}) << endl;
    return 0;
}
