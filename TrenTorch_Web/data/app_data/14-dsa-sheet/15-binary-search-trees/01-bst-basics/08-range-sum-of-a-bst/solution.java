class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space (recursion stack, h = tree height)
    static long rangeSumBst(TreeNode root, long low, long high) {
        if (root == null) {
            return 0;
        }
        if (root.val < low) {
            return rangeSumBst(root.right, low, high);
        }
        if (root.val > high) {
            return rangeSumBst(root.left, low, high);
        }
        return root.val
            + rangeSumBst(root.left, low, high)
            + rangeSumBst(root.right, low, high);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
