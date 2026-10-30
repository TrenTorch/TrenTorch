#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) extra space
fn remove_duplicates_sorted(mut head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut cur = head.as_mut();
    while let Some(node) = cur {
        while let Some(next_node) = node.next.as_mut() {
            if node.val == next_node.val {
                node.next = next_node.next.take();
            } else {
                break;
            }
        }
        cur = node.next.as_mut();
    }
    head
}

fn main() {
    // Call it here and print the result to try it.
}
