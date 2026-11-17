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


def reverse_between(head, left, size):
    values = to_list(head)
    part = values[left - 1 : left - 1 + size]
    return from_list(values[: left - 1] + part[::-1] + values[left - 1 + size :])
