#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn inorder_traversal(root: Option<Box<TreeNode>>) -> Vec<i64> {
    let mut out = Vec::new();
    let mut stack = Vec::new();
    let mut node = root.as_deref();
    while node.is_some() || !stack.is_empty() {
        while let Some(n) = node {
            stack.push(n);
            node = n.left.as_deref();
        }
        let n = stack.pop().unwrap();
        out.push(n.val);
        node = n.right.as_deref();
    }
    out
}

fn main() {
    // Call it here and print the result to try it.
}
