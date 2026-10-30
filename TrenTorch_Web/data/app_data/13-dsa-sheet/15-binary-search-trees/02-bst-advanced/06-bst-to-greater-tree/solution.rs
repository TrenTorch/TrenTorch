#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// Reverse inorder walk: visit larger values first, keeping a running total.
fn accumulate(node: Option<&mut TreeNode>, total: &mut i64) {
    if let Some(n) = node {
        accumulate(n.right.as_deref_mut(), total);
        *total += n.val;
        n.val = *total;
        accumulate(n.left.as_deref_mut(), total);
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn convert_bst(mut root: Option<Box<TreeNode>>) -> Option<Box<TreeNode>> {
    let mut total: i64 = 0;
    accumulate(root.as_deref_mut(), &mut total);
    root
}

fn main() {
    // Call it here and print the result to try it.
}
