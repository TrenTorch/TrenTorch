import java.util.Stack;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space where h is tree height
    static TreeNode recoverTree(TreeNode root) {
        TreeNode first = null, second = null, prev = null;
        Stack<TreeNode> stack = new Stack<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
            node = stack.pop();
            if (prev != null && prev.val > node.val) {
                if (first == null) {
                    first = prev;
                }
                second = node;
            }
            prev = node;
            node = node.right;
        }
        if (first != null && second != null) {
            long temp = first.val;
            first.val = second.val;
            second.val = temp;
        }
        return root;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
