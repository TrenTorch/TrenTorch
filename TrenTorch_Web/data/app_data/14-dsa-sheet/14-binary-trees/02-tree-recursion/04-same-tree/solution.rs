#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space
fn is_same_tree(p: Option<Box<TreeNode>>, q: Option<Box<TreeNode>>) -> bool {
    match (p, q) {
        (None, None) => true,
        (Some(p_node), Some(q_node)) => {
            if p_node.val != q_node.val {
                return false;
            }
            is_same_tree(p_node.left, q_node.left) && is_same_tree(p_node.right, q_node.right)
        }
        _ => false,
    }
}

fn main() {
    // Call it here and print the result to try it.
}
