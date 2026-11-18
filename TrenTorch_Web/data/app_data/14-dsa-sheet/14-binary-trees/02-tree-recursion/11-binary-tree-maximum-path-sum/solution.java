class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static long maxPathSum(TreeNode root) {
        long[] best = new long[]{root.val};
        gain(root, best);
        return best[0];
    }

    private static long gain(TreeNode node, long[] best) {
        if (node == null) return 0;
        long left = Math.max(0, gain(node.left, best));
        long right = Math.max(0, gain(node.right, best));
        best[0] = Math.max(best[0], node.val + left + right);
        return node.val + Math.max(left, right);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
