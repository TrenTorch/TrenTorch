class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def rotate_list(head: ListNode | None, k: int) -> ListNode | None:
    """Rotate the list to the right by k places."""
    # This is correct but too slow: it moves the last node to the front, k times.
    if not head or not head.next:
        return head
    for _ in range(k):
        prev = head
        while prev.next.next:
            prev = prev.next
        last = prev.next
        prev.next = None
        last.next = head
        head = last
    return head
