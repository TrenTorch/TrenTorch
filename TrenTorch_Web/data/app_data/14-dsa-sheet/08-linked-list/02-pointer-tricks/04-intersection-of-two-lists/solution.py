class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def intersection_node(list_a, list_b):
    pa, pb = list_a, list_b
    while pa is not pb:
        pa = pa.next if pa else list_b
        pb = pb.next if pb else list_a
    return pa
