#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn preorder_traversal(root: Option<Box<TreeNode>>) -> Vec<i64> {
    let mut out = Vec::new();
    let mut stack = Vec::new();
    if let Some(node) = root {
        stack.push(node);
    }
    while let Some(node) = stack.pop() {
        out.push(node.val);
        if let Some(right) = node.right {
            stack.push(right);
        }
        if let Some(left) = node.left {
            stack.push(left);
        }
    }
    out
}

fn main() {
    // Call it here and print the result to try it.
}
