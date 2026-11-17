class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function swapPairs(head) {
  const dummy = new ListNode(0, head);
  let prev = dummy;
  while (prev.next && prev.next.next) {
    const a = prev.next;
    const b = a.next;
    a.next = b.next;
    b.next = a;
    prev.next = b;
    prev = a;
  }
  return dummy.next;
}

// Example usage for manual testing:
function arrayToList(arr) {
  let head = null;
  let tail = null;
  for (const val of arr) {
    const node = new ListNode(val);
    if (!head) head = node;
    else tail.next = node;
    tail = node;
  }
  return head;
}

function listToArray(head) {
  const result = [];
  while (head) {
    result.push(head.val);
    head = head.next;
  }
  return result;
}

console.log(listToArray(swapPairs(arrayToList([1, 2, 3, 4])))); // [2, 1, 4, 3]
console.log(listToArray(swapPairs(arrayToList([1, 2, 3]))));    // [2, 1, 3]
console.log(listToArray(swapPairs(arrayToList([]))));            // []
console.log(listToArray(swapPairs(arrayToList([1]))));           // [1]
