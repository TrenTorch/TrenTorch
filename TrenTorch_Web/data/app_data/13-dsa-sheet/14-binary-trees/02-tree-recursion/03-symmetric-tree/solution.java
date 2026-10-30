class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space (recursion depth h)
    static boolean isSymmetric(TreeNode root) {
        return root == null || mirror(root.left, root.right);
    }

    private static boolean mirror(TreeNode a, TreeNode b) {
        if (a == null && b == null) {
            return true;
        }
        if (a == null || b == null || a.val != b.val) {
            return false;
        }
        return mirror(a.left, b.right) && mirror(a.right, b.left);
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
        System.out.println(isSymmetric(fromLevelOrder(new Long[]{1L, 2L, 2L, 3L, 4L, 4L, 3L})));
        System.out.println(isSymmetric(fromLevelOrder(new Long[]{1L, 2L, 2L, null, 3L, null, 3L})));
    }
}
