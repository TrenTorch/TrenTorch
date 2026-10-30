use std::ptr;

#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn has_cycle(head: Option<Box<ListNode>>) -> bool {
    let head_ref: Option<&ListNode> = head.as_deref();
    let mut slow = head_ref;
    let mut fast = head_ref;
    while let Some(f) = fast {
        let n = match f.next.as_deref() {
            Some(n) => n,
            None => return false,
        };
        fast = n.next.as_deref();
        slow = slow.and_then(|s| s.next.as_deref());
        if let (Some(s), Some(g)) = (slow, fast) {
            if ptr::eq(s, g) {
                return true;
            }
        }
    }
    false
}

fn main() {
    // Call it here and print the result to try it.
}
