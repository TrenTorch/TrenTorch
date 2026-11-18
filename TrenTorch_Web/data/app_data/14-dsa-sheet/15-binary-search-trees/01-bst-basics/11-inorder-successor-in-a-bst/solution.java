public class Main {
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // O(h) time, O(1) space where h is tree height
    public static TreeNode inorderSuccessor(TreeNode root, int p) {
        TreeNode answer = null;
        TreeNode node = root;
        while (node != null) {
            if (node.val > p) {
                answer = node;
                node = node.left;
            } else {
                node = node.right;
            }
        }
        return answer;
    }

    public static void main(String[] args) {
    }
}
