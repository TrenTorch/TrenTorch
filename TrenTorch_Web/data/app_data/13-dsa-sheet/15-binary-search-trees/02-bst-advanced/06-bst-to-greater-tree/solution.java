import java.util.Stack;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static TreeNode convertBst(TreeNode root) {
        long total = 0;
        Stack<TreeNode> stack = new Stack<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.right;
            }
            node = stack.pop();
            total += node.val;
            node.val = total;
            node = node.left;
        }
        return root;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
