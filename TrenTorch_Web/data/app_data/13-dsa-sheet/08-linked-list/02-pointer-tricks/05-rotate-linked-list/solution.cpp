#include <bits/stdc++.h>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x = 0, ListNode* n = nullptr) : val(x), next(n) {}
};

// O(n) time, O(1) space
ListNode* rotateList(ListNode* head, long long k) {
    if (!head || !head->next) return head;
    long long length = 1;
    ListNode* tail = head;
    while (tail->next) {
        tail = tail->next;
        length++;
    }
    k %= length;
    if (k == 0) return head;
    ListNode* newTail = head;
    for (long long i = 0; i < length - k - 1; i++) newTail = newTail->next;
    ListNode* newHead = newTail->next;
    newTail->next = nullptr;
    tail->next = head;
    return newHead;
}

int main() {
    // Call it here and print the result to try it.
    return 0;
}
