#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* removeElements(ListNode* head, long long val) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    ListNode* cur = head;
    while (cur) {
        if (cur->val == val) {
            prev->next = cur->next;
        } else {
            prev = cur;
        }
        cur = cur->next;
    }
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
