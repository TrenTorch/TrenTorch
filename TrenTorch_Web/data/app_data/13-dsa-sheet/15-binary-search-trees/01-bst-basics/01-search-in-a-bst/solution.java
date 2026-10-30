class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(h) time, O(1) space
    static TreeNode searchBst(TreeNode root, long val) {
        TreeNode node = root;
        while (node != null && node.val != val) {
            if (val < node.val) {
                node = node.left;
            } else {
                node = node.right;
            }
        }
        return node;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
