class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n + m) time, O(1) space
function mergeTwoLists(list1, list2) {
  const dummy = new ListNode();
  let tail = dummy;
  let a = list1;
  let b = list2;
  while (a && b) {
    if (a.val <= b.val) {
      tail.next = a;
      a = a.next;
    } else {
      tail.next = b;
      b = b.next;
    }
    tail = tail.next;
  }
  tail.next = a || b;
  return dummy.next;
}

// Call mergeTwoLists(...) here and console.log the result to try it.
