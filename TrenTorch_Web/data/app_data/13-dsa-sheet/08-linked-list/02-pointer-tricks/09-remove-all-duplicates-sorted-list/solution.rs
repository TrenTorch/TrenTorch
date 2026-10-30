#[derive(Debug)]
struct ListNode {
    val: i64,
    next: Option<Box<ListNode>>,
}

// O(n) time, O(1) space
fn remove_all_duplicates(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode { val: 0, next: head });
    let mut prev: &mut Box<ListNode> = &mut dummy;
    loop {
        let value = match prev.next.as_ref() {
            Some(n) => n.val,
            None => break,
        };
        let dup = prev
            .next
            .as_ref()
            .unwrap()
            .next
            .as_ref()
            .map_or(false, |nx| nx.val == value);
        if dup {
            while prev.next.as_ref().map_or(false, |n| n.val == value) {
                let mut n = prev.next.take().unwrap();
                prev.next = n.next.take();
            }
        } else {
            prev = prev.next.as_mut().unwrap();
        }
    }
    dummy.next
}

fn main() {
    // Call it here and print the result to try it.
}
