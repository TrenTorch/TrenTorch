class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(1) space
    static TreeNode flattenTree(TreeNode root) {
        TreeNode node = root;
        while (node != null) {
            if (node.left != null) {
                TreeNode tail = node.left;
                while (tail.right != null) {
                    tail = tail.right;
                }
                tail.right = node.right;
                node.right = node.left;
                node.left = null;
            }
            node = node.right;
        }
        return root;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
