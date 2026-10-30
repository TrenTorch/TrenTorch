class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space (recursion depth h)
    static boolean hasPathSum(TreeNode root, long target) {
        if (root == null) {
            return false;
        }
        if (root.left == null && root.right == null) {
            return root.val == target;
        }
        long rest = target - root.val;
        return hasPathSum(root.left, rest) || hasPathSum(root.right, rest);
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
        System.out.println(hasPathSum(fromLevelOrder(new Long[]{5L, 4L, 8L, 11L, null, 13L, 4L, 7L, 2L, null, null, null, 1L}), 22L));
        System.out.println(hasPathSum(fromLevelOrder(new Long[]{1L, 2L, 3L}), 5L));
    }
}
