use std::ptr;

#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(m + n) time, O(1) space
// Returns the position in list_a of the first shared node, or -1 if none.
fn intersection_node(list_a: Option<Box<ListNode>>, list_b: Option<Box<ListNode>>) -> i64 {
    let a_head: Option<&ListNode> = list_a.as_deref();
    let b_head: Option<&ListNode> = list_b.as_deref();
    let mut pa: Option<&ListNode> = a_head;
    let mut pb: Option<&ListNode> = b_head;
    loop {
        let same = match (pa, pb) {
            (Some(x), Some(y)) => ptr::eq(x, y),
            (None, None) => true,
            _ => false,
        };
        if same {
            break;
        }
        pa = match pa {
            Some(x) => x.next.as_deref(),
            None => b_head,
        };
        pb = match pb {
            Some(y) => y.next.as_deref(),
            None => a_head,
        };
    }
    let target: &ListNode = match pa {
        Some(t) => t,
        None => return -1,
    };
    let mut cur = a_head;
    let mut pos: i64 = 0;
    while let Some(c) = cur {
        if ptr::eq(c, target) {
            return pos;
        }
        cur = c.next.as_deref();
        pos += 1;
    }
    -1
}

fn main() {
}
