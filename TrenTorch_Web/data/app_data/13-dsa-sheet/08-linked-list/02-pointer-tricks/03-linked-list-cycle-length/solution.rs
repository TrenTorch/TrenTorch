use std::ptr;

#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn cycle_length(head: Option<Box<ListNode>>) -> i64 {
    let head_ref: Option<&ListNode> = head.as_deref();
    let mut slow = head_ref;
    let mut fast = head_ref;
    let mut meet: Option<&ListNode> = None;
    while let Some(f) = fast {
        let n = match f.next.as_deref() {
            Some(n) => n,
            None => break,
        };
        fast = n.next.as_deref();
        slow = slow.and_then(|s| s.next.as_deref());
        if let (Some(s), Some(g)) = (slow, fast) {
            if ptr::eq(s, g) {
                meet = Some(s);
                break;
            }
        }
    }
    let start: &ListNode = match meet {
        Some(m) => m,
        None => return 0,
    };
    let mut length: i64 = 1;
    let mut node = start.next.as_deref();
    while let Some(nd) = node {
        if ptr::eq(nd, start) {
            break;
        }
        node = nd.next.as_deref();
        length += 1;
    }
    length
}

fn main() {
    // Call it here and print the result to try it.
}
