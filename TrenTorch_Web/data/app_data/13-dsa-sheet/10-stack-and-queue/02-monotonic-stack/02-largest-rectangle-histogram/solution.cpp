#include <bits/stdc++.h>
using namespace std;

// O(n) time, O(n) space
long long largestRectangle(vector<long long> heights) {
    int n = heights.size();
    long long best = 0;
    vector<int> stack;
    for (int i = 0; i <= n; i++) {
        long long h = (i == n) ? 0 : heights[i];
        while (!stack.empty() && heights[stack.back()] >= h) {
            long long height = heights[stack.back()];
            stack.pop_back();
            int left = stack.empty() ? -1 : stack.back();
            best = max(best, height * (i - left - 1));
        }
        stack.push_back(i);
    }
    return best;
}

int main() {
    cout << largestRectangle(vector<long long>{2, 1, 5, 6, 2, 3}) << endl;
    return 0;
}
