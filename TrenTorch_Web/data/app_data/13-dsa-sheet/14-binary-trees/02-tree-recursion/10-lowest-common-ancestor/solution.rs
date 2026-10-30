// Write lowest_common_ancestor as the problem statement describes.

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

impl TreeNode {
    fn new(val: i64) -> Self {
        TreeNode { val, left: None, right: None }
    }
}

// O(n) time, O(h) space
fn lowest_common_ancestor(root: Option<&TreeNode>, p: i64, q: i64) -> Option<&TreeNode> {
    let root = root?;
    if root.val == p || root.val == q {
        return Some(root);
    }
    let left = lowest_common_ancestor(root.left.as_deref(), p, q);
    let right = lowest_common_ancestor(root.right.as_deref(), p, q);
    if left.is_some() && right.is_some() {
        Some(root)
    } else {
        left.or(right)
    }
}

fn main() {
}
