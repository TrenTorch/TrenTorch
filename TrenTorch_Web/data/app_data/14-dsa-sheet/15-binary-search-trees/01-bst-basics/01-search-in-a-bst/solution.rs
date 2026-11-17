#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(h) time, O(1) extra space where h is the height of the tree
fn search_bst(root: Option<Box<TreeNode>>, val: i64) -> Option<Box<TreeNode>> {
    let mut node = root;
    while let Some(mut n) = node {
        if n.val == val {
            return Some(n);
        }
        node = if val < n.val { n.left.take() } else { n.right.take() };
    }
    None
}

fn main() {
    // Call it here and print the result to try it.
}
