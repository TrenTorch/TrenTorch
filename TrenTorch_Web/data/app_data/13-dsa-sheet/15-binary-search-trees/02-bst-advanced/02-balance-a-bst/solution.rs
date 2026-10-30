#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn balance_bst(root: Option<Box<TreeNode>>) -> Option<Box<TreeNode>> {
    // Iterative inorder traversal to collect sorted values.
    let mut values = Vec::new();
    let mut stack = Vec::new();
    let mut current = root.as_deref();
    while current.is_some() || !stack.is_empty() {
        while let Some(node) = current {
            stack.push(node);
            current = node.left.as_deref();
        }
        if let Some(node) = stack.pop() {
            values.push(node.val);
            current = node.right.as_deref();
        }
    }

    // Recursively build a height-balanced BST from the sorted values.
    fn build_balanced(values: &[i64], lo: usize, hi: usize) -> Option<Box<TreeNode>> {
        if lo > hi {
            return None;
        }
        let mid = (lo + hi) / 2;
        Some(Box::new(TreeNode {
            val: values[mid],
            left: build_balanced(values, lo, mid - 1),
            right: build_balanced(values, mid + 1, hi),
        }))
    }

    if values.is_empty() {
        None
    } else {
        build_balanced(&values, 0, values.len() - 1)
    }
}

fn main() {
    // Call it here and print the result to try it.
}
