#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn find_min(node: &Option<Box<TreeNode>>) -> i64 {
    let mut cursor = node.as_ref().expect("node is not None");
    while let Some(left) = cursor.left.as_ref() {
        cursor = left;
    }
    cursor.val
}

// O(h) time, O(h) space where h is the height of the tree
fn delete_node(root: Option<Box<TreeNode>>, key: i64) -> Option<Box<TreeNode>> {
    match root {
        None => None,
        Some(mut node) => {
            if key < node.val {
                node.left = delete_node(node.left, key);
                Some(node)
            } else if key > node.val {
                node.right = delete_node(node.right, key);
                Some(node)
            } else {
                // Node to delete found
                if node.left.is_none() {
                    return node.right;
                }
                if node.right.is_none() {
                    return node.left;
                }
                // Both children exist: find inorder successor (smallest in right subtree)
                let successor_val = find_min(&node.right);
                // Delete the successor from right subtree and replace current node's value
                node.right = delete_node(node.right, successor_val);
                node.val = successor_val;
                Some(node)
            }
        }
    }
}

fn main() {
    // Call it here and print the result to try it.
}
