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


def reverse_k_group(head, k):
    values = to_list(head)
    out = []
    for i in range(0, len(values), k):
        block = values[i : i + k]
        out.extend(block[::-1] if len(block) == k else block)
    return from_list(out)
