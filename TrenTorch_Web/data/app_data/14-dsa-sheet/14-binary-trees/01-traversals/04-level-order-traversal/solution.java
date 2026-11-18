import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[][] levelOrder(TreeNode root) {
        if (root == null) {
            return new long[0][];
        }
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        List<long[]> result = new ArrayList<>();
        while (!queue.isEmpty()) {
            int size = queue.size();
            long[] level = new long[size];
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level[i] = node.val;
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            result.add(level);
        }
        return result.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
