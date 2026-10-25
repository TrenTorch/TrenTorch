class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def sort_list(head: ListNode | None) -> ListNode | None:
    """Sort the list in increasing order."""
    # This is correct but too slow: it is an insertion sort, which takes O(n^2) steps.
    dummy = ListNode()
    while head:
        after = head.next
        prev = dummy
        while prev.next and prev.next.val < head.val:
            prev = prev.next
        head.next = prev.next
        prev.next = head
        head = after
    return dummy.next
