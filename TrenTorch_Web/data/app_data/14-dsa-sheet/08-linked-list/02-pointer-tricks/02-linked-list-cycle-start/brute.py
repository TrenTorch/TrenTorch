class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def to_list(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


def from_list(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def cycle_start(head):
    seen = set()
    while head:
        if id(head) in seen:
            return head
        seen.add(id(head))
        head = head.next
    return None
