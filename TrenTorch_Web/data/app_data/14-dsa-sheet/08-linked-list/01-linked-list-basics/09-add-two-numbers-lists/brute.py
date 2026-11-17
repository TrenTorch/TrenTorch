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


def add_two_numbers(l1, l2):
    a = int("".join(map(str, to_list(l1)[::-1])))
    b = int("".join(map(str, to_list(l2)[::-1])))
    return from_list([int(ch) for ch in str(a + b)[::-1]])
