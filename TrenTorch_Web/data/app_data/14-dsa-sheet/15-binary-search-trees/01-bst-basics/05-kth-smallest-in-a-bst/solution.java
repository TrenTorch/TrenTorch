import java.util.ArrayDeque;
import java.util.Deque;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static long kthSmallestBst(TreeNode root, long k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
            node = stack.pop();
            k--;
            if (k == 0) {
                return node.val;
            }
            node = node.right;
        }
        // Should never reach here given constraints
        return -1;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
