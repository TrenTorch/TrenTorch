#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* removeAllDuplicates(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    ListNode* cur = head;
    while (cur) {
        if (cur->next && cur->next->val == cur->val) {
            int value = cur->val;
            while (cur && cur->val == value) cur = cur->next;
            prev->next = cur;
        } else {
            prev = cur;
            cur = cur->next;
        }
    }
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
