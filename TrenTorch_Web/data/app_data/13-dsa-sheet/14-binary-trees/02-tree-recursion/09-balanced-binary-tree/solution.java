class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space where h is tree height
    static boolean isBalanced(TreeNode root) {
        return check(root) != -1;
    }

    private static int check(TreeNode node) {
        if (node == null) return 0;
        int left = check(node.left);
        if (left == -1) return -1;
        int right = check(node.right);
        if (right == -1 || Math.abs(left - right) > 1) return -1;
        return 1 + Math.max(left, right);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
