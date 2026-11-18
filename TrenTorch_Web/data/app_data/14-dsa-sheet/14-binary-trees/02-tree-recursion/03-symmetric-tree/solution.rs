#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn mirror(a: Option<&TreeNode>, b: Option<&TreeNode>) -> bool {
    match (a, b) {
        (None, None) => true,
        (Some(x), Some(y)) => {
            x.val == y.val
                && mirror(x.left.as_deref(), y.right.as_deref())
                && mirror(x.right.as_deref(), y.left.as_deref())
        }
        _ => false,
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn is_symmetric(root: Option<Box<TreeNode>>) -> bool {
    match root {
        None => true,
        Some(r) => mirror(r.left.as_deref(), r.right.as_deref()),
    }
}

fn main() {
    // Call it here and print the result to try it.
}
