use std::ptr;

#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
// Returns the position of the cycle's first node, or -1 if there is no cycle.
fn cycle_start(head: Option<Box<ListNode>>) -> i64 {
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
    let meet: &ListNode = match meet {
        Some(m) => m,
        None => return -1,
    };
    let mut a: Option<&ListNode> = head_ref;
    let mut b: Option<&ListNode> = Some(meet);
    let mut pos: i64 = 0;
    loop {
        match (a, b) {
            (Some(x), Some(y)) => {
                if ptr::eq(x, y) {
                    return pos;
                }
                a = x.next.as_deref();
                b = y.next.as_deref();
                pos += 1;
            }
            _ => return -1,
        }
    }
}

fn main() {
}
