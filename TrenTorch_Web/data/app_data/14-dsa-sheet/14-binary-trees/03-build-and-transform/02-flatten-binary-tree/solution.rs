#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(1) extra space
fn flatten_tree(mut root: Option<Box<TreeNode>>) -> Option<Box<TreeNode>> {
    let mut cur = root.as_deref_mut();
    while let Some(node) = cur {
        if let Some(mut left) = node.left.take() {
            let mut tail: &mut TreeNode = &mut left;
            while tail.right.is_some() {
                tail = tail.right.as_deref_mut().unwrap();
            }
            tail.right = node.right.take();
            node.right = Some(left);
        }
        cur = node.right.as_deref_mut();
    }
    root
}

fn main() {
    // Call it here and print the result to try it.
}
