import java.util.Stack;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static boolean findTarget(TreeNode root, long k) {
        if (root == null) return false;

        class BSTIterator {
            Stack<TreeNode> stack = new Stack<>();
            TreeNode current;
            boolean forward; // true: ascending (left->right), false: descending (right->left)

            BSTIterator(TreeNode root, boolean forward) {
                this.forward = forward;
                this.current = root;
            }

            boolean hasNext() {
                return current != null || !stack.isEmpty();
            }

            long next() {
                while (current != null) {
                    stack.push(current);
                    current = forward ? current.left : current.right;
                }
                current = stack.pop();
                long val = current.val;
                current = forward ? current.right : current.left;
                return val;
            }
        }

        BSTIterator loIter = new BSTIterator(root, true);
        BSTIterator hiIter = new BSTIterator(root, false);

        long lo = loIter.next();
        long hi = hiIter.next();

        while (lo < hi) {
            long sum = lo + hi;
            if (sum == k) {
                return true;
            } else if (sum < k) {
                if (loIter.hasNext()) {
                    lo = loIter.next();
                } else {
                    break;
                }
            } else {
                if (hiIter.hasNext()) {
                    hi = hiIter.next();
                } else {
                    break;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
