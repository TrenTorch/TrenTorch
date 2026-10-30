use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// O(n) time, O(n) space
fn burn_time(root: Option<Box<TreeNode>>, start: i64) -> i64 {
    let mut adj: HashMap<i64, Vec<i64>> = HashMap::new();
    let mut stack: Vec<(&TreeNode, Option<i64>)> = Vec::new();
    if let Some(node) = root.as_deref() {
        stack.push((node, None));
    }
    while let Some((node, parent_val)) = stack.pop() {
        let val = node.val;
        if let Some(p) = parent_val {
            adj.entry(val).or_default().push(p);
            adj.entry(p).or_default().push(val);
        }
        if let Some(left) = node.left.as_deref() {
            stack.push((left, Some(val)));
        }
        if let Some(right) = node.right.as_deref() {
            stack.push((right, Some(val)));
        }
    }

    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    visited.insert(start);
    queue.push_back(start);
    let mut minutes = -1;
    while !queue.is_empty() {
        minutes += 1;
        for _ in 0..queue.len() {
            let cur = queue.pop_front().unwrap();
            if let Some(neighbors) = adj.get(&cur) {
                for &nxt in neighbors {
                    if !visited.contains(&nxt) {
                        visited.insert(nxt);
                        queue.push_back(nxt);
                    }
                }
            }
        }
    }
    minutes
}

fn main() {
    // Call it here and print the result to try it.
}
