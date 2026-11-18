class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def intersection_node(
    list_a: ListNode | None, list_b: ListNode | None
) -> ListNode | None:
    """Return the first node the two lists share, or None."""
    # This is correct but too slow: it compares every node of one list with every node of the other.
    a = list_a
    while a:
        b = list_b
        while b:
            if a is b:
                return a
            b = b.next
        a = a.next
    return None
