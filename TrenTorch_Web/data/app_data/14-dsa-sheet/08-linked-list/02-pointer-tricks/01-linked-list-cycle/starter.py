class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode | None) -> bool:
    """Return True if following next pointers never reaches the end."""
    # This is correct but too slow: it keeps the visited nodes in a list and searches the list at every step.
    seen = []
    while head:
        if head in seen:
            return True
        seen.append(head)
        head = head.next
    return False
