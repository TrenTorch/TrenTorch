#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space
fn middle_node(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    // Slow/fast walk on shared references: `steps` is how far slow moves.
    let mut steps = 0usize;
    let mut fast: Option<&ListNode> = head.as_deref();
    while let Some(f) = fast {
        match f.next.as_deref() {
            Some(f1) => {
                fast = f1.next.as_deref();
                steps += 1;
            }
            None => break,
        }
    }
    // Move ownership forward `steps` nodes to reach the middle.
    let mut cur = head;
    for _ in 0..steps {
        let node = *cur.expect("steps stay within the list");
        cur = node.next;
    }
    cur
}

fn main() {
    // Call it here and print the result to try it.
}
