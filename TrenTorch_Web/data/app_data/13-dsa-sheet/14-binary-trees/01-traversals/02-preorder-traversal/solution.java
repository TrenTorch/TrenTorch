import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[] preorderTraversal(TreeNode root) {
        if (root == null) return new long[0];
        List<Long> out = new ArrayList<>();
        ArrayDeque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            out.add(node.val);
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
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
