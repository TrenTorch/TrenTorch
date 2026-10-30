#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* partitionList(ListNode* head, long long x) {
    ListNode smallDummy;
    ListNode largeDummy;
    ListNode* smallTail = &smallDummy;
    ListNode* largeTail = &largeDummy;
    while (head) {
        if (head->val < x) {
            smallTail->next = head;
            smallTail = head;
        } else {
            largeTail->next = head;
            largeTail = head;
        }
        head = head->next;
    }
    largeTail->next = nullptr;
    smallTail->next = largeDummy.next;
    return smallDummy.next;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
