class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function partitionList(head, x) {
  const smallDummy = new ListNode();
  const largeDummy = new ListNode();
  let smallTail = smallDummy;
  let largeTail = largeDummy;

  while (head) {
    if (head.val < x) {
      smallTail.next = head;
      smallTail = head;
    } else {
      largeTail.next = head;
      largeTail = head;
    }
    head = head.next;
  }

  largeTail.next = null;
  smallTail.next = largeDummy.next;
  return smallDummy.next;
}

// Call partitionList(...) here and console.log the result to try it.
