#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space where h is the height of the tree
fn invert_tree(root: Option<Box<TreeNode>>) -> Option<Box<TreeNode>> {
    match root {
        None => None,
        Some(mut node) => {
            let left = invert_tree(node.left.take());
            let right = invert_tree(node.right.take());
            node.left = right;
            node.right = left;
            Some(node)
        }
    }
}

fn main() {
    // Call it here and print the result to try it.
}
