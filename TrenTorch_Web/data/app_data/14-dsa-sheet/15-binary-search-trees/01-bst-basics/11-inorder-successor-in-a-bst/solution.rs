#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i64,
    pub left: Option<Box<TreeNode>>,
    pub right: Option<Box<TreeNode>>,
}

// O(h) time, O(1) space where h is tree height
fn inorder_successor(root: Option<&Box<TreeNode>>, p: i64) -> Option<&TreeNode> {
    let mut answer = None;
    let mut node = root;
    while let Some(n) = node {
        if n.val > p {
            answer = Some(n.as_ref());
            node = n.left.as_ref();
        } else {
            node = n.right.as_ref();
        }
    }
    answer
}

fn main() {
}
