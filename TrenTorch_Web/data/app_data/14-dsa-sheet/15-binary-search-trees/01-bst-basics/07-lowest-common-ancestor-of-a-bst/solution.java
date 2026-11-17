class TreeNode {
    long val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(long val) { this.val = val; }
    TreeNode(long val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

public class Main {
    // O(h) time, O(1) space
    public static TreeNode lcaBst(TreeNode root, long p, long q) {
        TreeNode node = root;
        while (node != null) {
            if (p < node.val && q < node.val) {
                node = node.left;
            } else if (p > node.val && q > node.val) {
                node = node.right;
            } else {
                return node;
            }
        }
        return null;
    }

    public static void main(String[] args) {
    }
}
