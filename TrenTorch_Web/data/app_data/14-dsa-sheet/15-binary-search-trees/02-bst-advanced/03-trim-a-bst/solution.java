class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static TreeNode trimBst(TreeNode root, long low, long high) {
        if (root == null) {
            return null;
        }
        if (root.val < low) {
            return trimBst(root.right, low, high);
        }
        if (root.val > high) {
            return trimBst(root.left, low, high);
        }
        root.left = trimBst(root.left, low, high);
        root.right = trimBst(root.right, low, high);
        return root;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
