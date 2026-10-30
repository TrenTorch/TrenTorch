class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[][] zigzagLevelOrder(TreeNode root) {
        if (root == null) {
            return new long[0][];
        }
        java.util.List<long[]> out = new java.util.ArrayList<>();
        java.util.ArrayDeque<TreeNode> queue = new java.util.ArrayDeque<>();
        queue.add(root);
        boolean leftToRight = true;
        while (!queue.isEmpty()) {
            int size = queue.size();
            long[] level = new long[size];
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level[i] = node.val;
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
            if (!leftToRight) {
                for (int a = 0, b = size - 1; a < b; a++, b--) {
                    long tmp = level[a];
                    level[a] = level[b];
                    level[b] = tmp;
                }
            }
            out.add(level);
            leftToRight = !leftToRight;
        }
        return out.toArray(new long[0][]);
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
        System.out.println(java.util.Arrays.deepToString(zigzagLevelOrder(fromLevelOrder(new Long[]{3L, 9L, 20L, null, null, 15L, 7L}))));
        System.out.println(java.util.Arrays.deepToString(zigzagLevelOrder(fromLevelOrder(new Long[]{1L, 2L, 3L, 4L, null, null, 5L}))));
    }
}
