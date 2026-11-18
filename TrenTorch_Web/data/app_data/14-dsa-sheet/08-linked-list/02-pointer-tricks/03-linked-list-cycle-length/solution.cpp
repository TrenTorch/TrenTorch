#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
long long cycleLength(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            long long length = 1;
            ListNode* node = slow->next;
            while (node != slow) {
                node = node->next;
                length++;
            }
            return length;
        }
    }
    return 0;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
