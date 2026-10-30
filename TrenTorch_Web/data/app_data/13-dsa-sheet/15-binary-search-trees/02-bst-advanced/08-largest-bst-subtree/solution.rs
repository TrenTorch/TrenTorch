#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(h) space where h is tree height (≤ 800)
fn largest_bst_subtree(root: Option<Box<TreeNode>>) -> i64 {
    fn dfs(node: &Option<Box<TreeNode>>, best: &mut i64) -> (i64, i64, i64) {
        match node {
            None => (0, i64::MAX, i64::MIN),
            Some(n) => {
                let (left_size, left_low, left_high) = dfs(&n.left, best);
                let (right_size, right_low, right_high) = dfs(&n.right, best);
                if left_size >= 0 && right_size >= 0 && left_high < n.val && n.val < right_low {
                    let size = left_size + right_size + 1;
                    *best = (*best).max(size);
                    (size, left_low.min(n.val), right_high.max(n.val))
                } else {
                    (-1, i64::MIN, i64::MAX)
                }
            }
        }
    }

    let mut best = 0;
    dfs(&root, &mut best);
    best
}

fn main() {
    // Call it here and print the result to try it.
}
