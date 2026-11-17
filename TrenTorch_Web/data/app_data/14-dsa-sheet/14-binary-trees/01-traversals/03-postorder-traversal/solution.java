import java.util.ArrayList;
import java.util.Collections;
import java.util.Deque;
import java.util.ArrayDeque;
import java.util.List;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[] postorderTraversal(TreeNode root) {
        if (root == null) {
            return new long[0];
        }
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        List<Long> out = new ArrayList<>();
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            out.add(node.val);
            if (node.left != null) {
                stack.push(node.left);
            }
            if (node.right != null) {
                stack.push(node.right);
            }
        }
        Collections.reverse(out);
        long[] result = new long[out.size()];
        for (int i = 0; i < out.size(); i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
