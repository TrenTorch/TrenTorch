class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(h) time, O(1) space (h = tree height)
    static long[] floorAndCeilBst(TreeNode root, long x) {
        long floor = -1;
        long ceil = -1;
        TreeNode node = root;
        while (node != null) {
            if (node.val == x) {
                return new long[]{x, x};
            }
            if (node.val < x) {
                floor = node.val;
                node = node.right;
            } else {
                ceil = node.val;
                node = node.left;
            }
        }
        return new long[]{floor, ceil};
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
