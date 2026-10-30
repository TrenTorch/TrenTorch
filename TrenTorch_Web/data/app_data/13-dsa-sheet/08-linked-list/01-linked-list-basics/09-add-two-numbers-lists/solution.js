class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(max(n, m)) time, O(max(n, m)) space
function addTwoNumbers(l1, l2) {
  const dummy = new ListNode();
  let tail = dummy;
  let carry = 0;
  while (l1 || l2 || carry) {
    let total = carry;
    if (l1) {
      total += l1.val;
      l1 = l1.next;
    }
    if (l2) {
      total += l2.val;
      l2 = l2.next;
    }
    tail.next = new ListNode(total % 10);
    tail = tail.next;
    carry = Math.floor(total / 10);
  }
  return dummy.next;
}

// Call addTwoNumbers(...) here and console.log the result to try it.
