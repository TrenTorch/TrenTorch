use std::cmp::Reverse;
use std::collections::BinaryHeap;

#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n log k) time, O(k) space
fn merge_k_lists(mut lists: Vec<Option<Box<ListNode>>>) -> Option<Box<ListNode>> {
    let mut heap: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    for (i, l) in lists.iter().enumerate() {
        if let Some(node) = l {
            heap.push(Reverse((node.val, i)));
        }
    }
    let mut dummy = Box::new(ListNode { val: 0, next: None });
    let mut tail: &mut Box<ListNode> = &mut dummy;
    while let Some(Reverse((_, i))) = heap.pop() {
        let mut node = lists[i].take().unwrap();
        lists[i] = node.next.take();
        if let Some(next) = lists[i].as_ref() {
            heap.push(Reverse((next.val, i)));
        }
        tail.next = Some(node);
        tail = tail.next.as_mut().unwrap();
    }
    dummy.next
}

fn main() {
}
