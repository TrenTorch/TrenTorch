class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(h) time, O(1) space (h = tree height)
    static long closestValue(TreeNode root, long target) {
        long best = root.val;
        TreeNode node = root;
        while (node != null) {
            long dNode = Math.abs(node.val - target);
            long dBest = Math.abs(best - target);
            if (dNode < dBest || (dNode == dBest && node.val < best)) {
                best = node.val;
            }
            node = target < node.val ? node.left : node.right;
        }
        return best;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
