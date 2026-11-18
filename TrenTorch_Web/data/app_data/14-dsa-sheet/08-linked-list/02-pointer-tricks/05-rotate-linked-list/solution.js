class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

// O(n) time, O(1) space
function rotateList(head, k) {
  if (!head || !head.next) {
    return head;
  }
  let length = 1;
  let tail = head;
  while (tail.next) {
    tail = tail.next;
    length++;
  }
  k %= length;
  if (k === 0) {
    return head;
  }
  let newTail = head;
  for (let i = 0; i < length - k - 1; i++) {
    newTail = newTail.next;
  }
  const newHead = newTail.next;
  newTail.next = null;
  tail.next = head;
  return newHead;
}

// Call rotateList(...) here and console.log the result to try it.
function listToArray(head) {
  const arr = [];
  while (head) {
    arr.push(head.val);
    head = head.next;
  }
  return arr;
}

function arrayToList(arr) {
  if (arr.length === 0) return null;
  const head = new ListNode(arr[0]);
  let curr = head;
  for (let i = 1; i < arr.length; i++) {
    curr.next = new ListNode(arr[i]);
    curr = curr.next;
  }
  return head;
}

// Example 1
const head1 = arrayToList([1, 2, 3, 4, 5]);
const rotated1 = rotateList(head1, 2);
console.log(listToArray(rotated1)); // [4, 5, 1, 2, 3]

// Example 2
const head2 = arrayToList([0, 1, 2]);
const rotated2 = rotateList(head2, 4);
console.log(listToArray(rotated2)); // [2, 0, 1]
