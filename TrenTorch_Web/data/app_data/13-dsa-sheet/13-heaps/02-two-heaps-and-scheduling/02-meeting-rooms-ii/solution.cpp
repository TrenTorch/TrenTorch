#include <bits/stdc++.h>
using namespace std;

// O(n log n) time, O(n) space
long long minMeetingRooms(vector<vector<long long>> meetings) {
    sort(meetings.begin(), meetings.end());
    priority_queue<long long, vector<long long>, greater<long long>> rooms;  // end times of rooms in use
    for (auto& m : meetings) {
        long long start = m[0];
        long long end = m[1];
        if (!rooms.empty() && rooms.top() <= start) {
            rooms.pop();
            rooms.push(end);
        } else {
            rooms.push(end);
        }
    }
    return (long long)rooms.size();
}

int main() {
    cout << minMeetingRooms(vector<vector<long long>>{vector<long long>{0, 30}, vector<long long>{5, 10}, vector<long long>{15, 20}}) << endl;
    return 0;
}
