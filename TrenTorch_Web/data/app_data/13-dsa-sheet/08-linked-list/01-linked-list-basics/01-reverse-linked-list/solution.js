class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function reverseList(head) {
  let prev = null;
  while (head !== null) {
    const after = head.next;
    head.next = prev;
    prev = head;
    head = after;
  }
  return prev;
}

// Call reverseList(...) here and console.log the result to try it.
