#[derive(Debug)]
struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

// Yields the values in increasing order (inorder traversal, lazily).
struct Ascending<'a> {
    stack: Vec<&'a TreeNode>,
    node: Option<&'a TreeNode>,
}

impl<'a> Iterator for Ascending<'a> {
    type Item = i64;

    fn next(&mut self) -> Option<i64> {
        while let Some(n) = self.node {
            self.stack.push(n);
            self.node = n.left.as_deref();
        }
        let n = self.stack.pop()?;
        self.node = n.right.as_deref();
        Some(n.val)
    }
}

// Yields the values in decreasing order (reverse inorder, lazily).
struct Descending<'a> {
    stack: Vec<&'a TreeNode>,
    node: Option<&'a TreeNode>,
}

impl<'a> Iterator for Descending<'a> {
    type Item = i64;

    fn next(&mut self) -> Option<i64> {
        while let Some(n) = self.node {
            self.stack.push(n);
            self.node = n.right.as_deref();
        }
        let n = self.stack.pop()?;
        self.node = n.left.as_deref();
        Some(n.val)
    }
}

// O(n) time, O(h) space where h is the height of the tree
fn find_target(root: Option<Box<TreeNode>>, k: i64) -> bool {
    let mut up = Ascending {
        stack: Vec::new(),
        node: root.as_deref(),
    };
    let mut down = Descending {
        stack: Vec::new(),
        node: root.as_deref(),
    };
    let mut lo = up.next();
    let mut hi = down.next();
    while let (Some(a), Some(b)) = (lo, hi) {
        if a >= b {
            break;
        }
        let total = a + b;
        if total == k {
            return true;
        }
        if total < k {
            lo = up.next();
        } else {
            hi = down.next();
        }
    }
    false
}

fn main() {
    // Call it here and print the result to try it.
}
