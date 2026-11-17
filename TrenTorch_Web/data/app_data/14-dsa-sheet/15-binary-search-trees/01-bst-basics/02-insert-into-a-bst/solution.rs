#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(h) time, O(1) space where h is tree height
fn insert_into_bst(mut root: Option<Box<TreeNode>>, val: i64) -> Option<Box<TreeNode>> {
    let mut current = &mut root;
    while let Some(node) = current {
        if val < node.val {
            current = &mut node.left;
        } else {
            current = &mut node.right;
        }
    }
    *current = Some(Box::new(TreeNode { val, left: None, right: None }));
    root
}

fn main() {
    // Call it here and print the result to try it.
}
