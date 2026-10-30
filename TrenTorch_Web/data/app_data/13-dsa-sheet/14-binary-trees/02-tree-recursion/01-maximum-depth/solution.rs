#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

use std::cmp::max;

// O(n) time, O(h) space where h is tree height (recursion stack)
fn max_depth(root: Option<Box<TreeNode>>) -> i64 {
    match root {
        None => 0,
        Some(node) => 1 + max(max_depth(node.left), max_depth(node.right)),
    }
}

fn main() {
    // Call it here and print the result to try it.
}
