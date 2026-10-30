// O(n) time, O(1) space
function intersectionNode(listA, listB) {
  let pa = listA;
  let pb = listB;
  while (pa !== pb) {
    pa = pa ? pa.next : listB;
    pb = pb ? pb.next : listA;
  }
  return pa;
}
