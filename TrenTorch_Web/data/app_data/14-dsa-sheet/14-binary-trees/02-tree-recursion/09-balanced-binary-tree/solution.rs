#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// Height of the subtree, or -1 as soon as an unbalanced node is found.
fn check(node: Option<&TreeNode>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let left = check(n.left.as_deref());
            if left == -1 {
                return -1;
            }
            let right = check(n.right.as_deref());
            if right == -1 || (left - right).abs() > 1 {
                return -1;
            }
            1 + left.max(right)
        }
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn is_balanced(root: Option<Box<TreeNode>>) -> bool {
    check(root.as_deref()) != -1
}

fn main() {
    // Call it here and print the result to try it.
}
