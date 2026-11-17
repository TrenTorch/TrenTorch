class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space (queue holds at most one level)
    // Indices are kept relative to the first node of each level, so they never grow beyond the level width.
    static long widthOfTree(TreeNode root) {
        if (root == null) {
            return 0;
        }
        long best = 0;
        java.util.ArrayDeque<TreeNode> nodes = new java.util.ArrayDeque<>();
        java.util.ArrayDeque<Long> idxs = new java.util.ArrayDeque<>();
        nodes.add(root);
        idxs.add(0L);
        while (!nodes.isEmpty()) {
            int size = nodes.size();
            long first = idxs.peekFirst();
            long last = 0;
            for (int k = 0; k < size; k++) {
                TreeNode node = nodes.poll();
                long index = idxs.poll() - first;
                last = index;
                if (node.left != null) {
                    nodes.add(node.left);
                    idxs.add(2 * index + 1);
                }
                if (node.right != null) {
                    nodes.add(node.right);
                    idxs.add(2 * index + 2);
                }
            }
            best = Math.max(best, last + 1);
        }
        return best;
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
        System.out.println(widthOfTree(fromLevelOrder(new Long[]{1L, 3L, 2L, 5L, 3L, null, 9L})));
        System.out.println(widthOfTree(fromLevelOrder(new Long[]{1L, 3L, 2L, 5L})));
    }
}
