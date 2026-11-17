class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space (recursion depth h)
    static long diameter(TreeNode root) {
        long[] best = {0L};
        height(root, best);
        return best[0];
    }

    // Returns the height of node (in nodes) and updates best with the longest path through it.
    private static long height(TreeNode node, long[] best) {
        if (node == null) {
            return 0;
        }
        long left = height(node.left, best);
        long right = height(node.right, best);
        best[0] = Math.max(best[0], left + right);
        return 1 + Math.max(left, right);
    }

    // Builds a tree from a level-order list with null for missing children.
    static TreeNode fromLevelOrder(Long[] vals) {
        if (vals.length == 0 || vals[0] == null) {
            return null;
        }
        TreeNode root = new TreeNode(vals[0]);
        java.util.ArrayDeque<TreeNode> queue = new java.util.ArrayDeque<>();
        queue.add(root);
        int i = 1;
        while (!queue.isEmpty() && i < vals.length) {
            TreeNode node = queue.poll();
            Long lv = vals[i++];
            if (lv != null) {
                node.left = new TreeNode(lv);
                queue.add(node.left);
            }
            if (i < vals.length) {
                Long rv = vals[i++];
                if (rv != null) {
                    node.right = new TreeNode(rv);
                    queue.add(node.right);
                }
            }
        }
        return root;
    }

    public static void main(String[] args) {
        System.out.println(diameter(fromLevelOrder(new Long[]{1L, 2L, 3L, 4L, 5L})));
        System.out.println(diameter(fromLevelOrder(new Long[]{1L, 2L})));
    }
}
