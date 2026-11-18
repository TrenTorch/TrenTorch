#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space (second half is reversed in place)
fn is_palindrome_list(head: Option<Box<ListNode>>) -> bool {
    // Slow/fast walk on shared references: `skip` is the slow pointer's index.
    let mut skip = 0usize;
    let mut fast: Option<&ListNode> = head.as_deref();
    while let Some(f) = fast {
        match f.next.as_deref() {
            Some(f1) => {
                fast = f1.next.as_deref();
                skip += 1;
            }
            None => break,
        }
    }
    // Detach the second half, starting at the slow pointer.
    let mut left = head;
    let mut cursor: &mut Option<Box<ListNode>> = &mut left;
    for _ in 0..skip {
        cursor = &mut cursor.as_mut().unwrap().next;
    }
    let mut right = cursor.take();
    // Reverse the second half.
    let mut reversed: Option<Box<ListNode>> = None;
    while let Some(mut node) = right {
        right = node.next.take();
        node.next = reversed;
        reversed = Some(node);
    }
    // Compare the first half with the reversed second half.
    let mut lcur = left.as_deref();
    let mut rcur = reversed.as_deref();
    while let (Some(ln), Some(rn)) = (lcur, rcur) {
        if ln.val != rn.val {
            return false;
        }
        lcur = ln.next.as_deref();
        rcur = rn.next.as_deref();
    }
    true
}

fn main() {
    // Call it here and print the result to try it.
}
