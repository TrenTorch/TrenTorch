// Write lca_bst as the problem statement describes.

#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i64,
    pub left: Option<Box<TreeNode>>,
    pub right: Option<Box<TreeNode>>,
}

impl TreeNode {
    pub fn new(val: i64) -> Self {
        TreeNode { val, left: None, right: None }
    }
}

// O(h) time, O(1) space where h is the height of the tree
pub fn lca_bst(mut root: Option<Box<TreeNode>>, p: i64, q: i64) -> Option<Box<TreeNode>> {
    while let Some(node) = root {
        if p < node.val && q < node.val {
            root = node.left;
        } else if p > node.val && q > node.val {
            root = node.right;
        } else {
            return Some(node);
        }
    }
    None
}

fn main() {
}
