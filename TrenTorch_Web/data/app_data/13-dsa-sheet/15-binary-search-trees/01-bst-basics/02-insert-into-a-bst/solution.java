class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(h) time, O(1) space (h = tree height)
    static TreeNode insertIntoBst(TreeNode root, long val) {
        if (root == null) {
            return new TreeNode(val);
        }
        TreeNode node = root;
        while (true) {
            if (val < node.val) {
                if (node.left == null) {
                    node.left = new TreeNode(val);
                    break;
                }
                node = node.left;
            } else {
                if (node.right == null) {
                    node.right = new TreeNode(val);
                    break;
                }
                node = node.right;
            }
        }
        return root;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
