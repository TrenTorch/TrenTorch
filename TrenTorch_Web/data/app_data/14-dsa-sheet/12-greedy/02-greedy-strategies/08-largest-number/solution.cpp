#include <bits/stdc++.h>
using namespace std;

// O(n log n * L) time where L is the max digit count, O(n * L) space
string largestNumber(vector<long long> nums) {
    vector<string> strs;
    strs.reserve(nums.size());
    for (long long x : nums) strs.push_back(to_string(x));
    sort(strs.begin(), strs.end(), [](const string& a, const string& b) {
        return a + b > b + a;
    });
    string result;
    for (const auto& s : strs) result += s;
    if (result.empty() || result[0] == '0') return "0";
    return result;
}

int main() {
    cout << largestNumber(vector<long long>{10, 2}) << endl;
    return 0;
}
