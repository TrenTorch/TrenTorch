import java.util.ArrayDeque;
import java.util.Deque;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static long minDiffBst(TreeNode root) {
        long best = Long.MAX_VALUE;
        Long prev = null;
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
            node = stack.pop();
            if (prev != null) {
                long diff = node.val - prev;
                if (diff < best) best = diff;
            }
            prev = node.val;
            node = node.right;
        }
        return best;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
