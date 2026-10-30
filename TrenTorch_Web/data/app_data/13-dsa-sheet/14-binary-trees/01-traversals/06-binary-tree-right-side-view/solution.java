import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[] rightSideView(TreeNode root) {
        if (root == null) {
            return new long[0];
        }
        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        List<Long> result = new ArrayList<>();
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            long lastVal = 0;
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                lastVal = node.val;
                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }
            result.add(lastVal);
        }
        long[] arr = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            arr[i] = result.get(i);
        }
        return arr;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
