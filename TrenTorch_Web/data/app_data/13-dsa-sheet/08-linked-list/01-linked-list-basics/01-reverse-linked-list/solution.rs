#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space
fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut prev: Option<Box<ListNode>> = None;
    let mut cur = head;
    while let Some(mut node) = cur {
        cur = node.next.take();
        node.next = prev;
        prev = Some(node);
    }
    prev
}

fn main() {
    // Call it here and print the result to try it.
}
