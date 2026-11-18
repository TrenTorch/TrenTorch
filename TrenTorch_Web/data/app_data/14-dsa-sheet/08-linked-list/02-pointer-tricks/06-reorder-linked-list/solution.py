class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reorder_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    prev = None
    while second:
        after = second.next
        second.next = prev
        prev = second
        second = after
    first, second = head, prev
    while second:
        a, b = first.next, second.next
        first.next = second
        second.next = a
        first, second = a, b
    return head
