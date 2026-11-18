#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(max(n, m)) time, O(max(n, m)) space for the new list
ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
    ListNode dummy;
    ListNode* tail = &dummy;
    int carry = 0;
    while (l1 || l2 || carry) {
        int total = carry;
        if (l1) {
            total += l1->val;
            l1 = l1->next;
        }
        if (l2) {
            total += l2->val;
            l2 = l2->next;
        }
        tail->next = new ListNode(total % 10);
        tail = tail->next;
        carry = total / 10;
    }
    return dummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
