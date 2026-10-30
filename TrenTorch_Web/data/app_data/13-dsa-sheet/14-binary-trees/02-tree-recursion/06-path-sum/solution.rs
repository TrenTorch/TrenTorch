// O(n) time, O(h) space (h = tree height, max 800)

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn has_path_sum(root: Option<Box<TreeNode>>, target: i64) -> bool {
    match root {
        None => false,
        Some(node) => {
            let left = node.left;
            let right = node.right;
            let val = node.val;

            if left.is_none() && right.is_none() {
                return val == target;
            }

            let rest = target - val;
            has_path_sum(left, rest) || has_path_sum(right, rest)
        }
    }
}

fn main() {
    // Call it here and print the result to try it.
}
