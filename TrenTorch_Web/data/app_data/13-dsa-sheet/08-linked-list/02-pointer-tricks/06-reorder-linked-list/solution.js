class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function reorderList(head) {
  if (!head || !head.next) {
    return head;
  }
  let slow = head;
  let fast = head.next;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
  }
  let second = slow.next;
  slow.next = null;
  let prev = null;
  while (second) {
    const after = second.next;
    second.next = prev;
    prev = second;
    second = after;
  }
  let first = head;
  second = prev;
  while (second) {
    const a = first.next;
    const b = second.next;
    first.next = second;
    second.next = a;
    first = a;
    second = b;
  }
  return head;
}

// Call reorderList(...) here and console.log the result to try it.
