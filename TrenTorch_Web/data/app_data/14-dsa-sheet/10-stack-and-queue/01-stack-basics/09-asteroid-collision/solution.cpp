#include <bits/stdc++.h>
using namespace std;

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    os << "[";
    for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i];
    return os << "]";
}

// O(n) time, O(n) space
vector<long long> asteroidCollision(vector<long long> asteroids) {
    vector<long long> stk;
    for (long long a : asteroids) {
        bool alive = true;
        while (alive && a < 0 && !stk.empty() && stk.back() > 0) {
            if (stk.back() < -a) {
                stk.pop_back();
            } else if (stk.back() == -a) {
                stk.pop_back();
                alive = false;
            } else {
                alive = false;
            }
        }
        if (alive) stk.push_back(a);
    }
    return stk;
}

int main() {
    cout << asteroidCollision(vector<long long>{5, 10, -5}) << endl;
    return 0;
}
