class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space (h = tree height, up to 800)
    static boolean isValidBst(TreeNode root) {
        return check(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    static boolean check(TreeNode node, long low, long high) {
        if (node == null) {
            return true;
        }
        if (!(low < node.val && node.val < high)) {
            return false;
        }
        return check(node.left, low, node.val) && check(node.right, node.val, high);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
