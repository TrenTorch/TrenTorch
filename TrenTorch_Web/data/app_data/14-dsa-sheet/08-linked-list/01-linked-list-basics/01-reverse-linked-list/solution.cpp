#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* after = head->next;
        head->next = prev;
        prev = head;
        head = after;
    }
    return prev;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
