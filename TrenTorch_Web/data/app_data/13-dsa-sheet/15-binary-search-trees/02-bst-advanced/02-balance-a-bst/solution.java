import java.util.ArrayDeque;
import java.util.ArrayList;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space (sorted values list, plus O(log n) recursion)
    static TreeNode balanceBst(TreeNode root) {
        ArrayList<Long> values = new ArrayList<>();
        ArrayDeque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
            node = stack.pop();
            values.add(node.val);
            node = node.right;
        }
        long[] sorted = new long[values.size()];
        for (int i = 0; i < sorted.length; i++) {
            sorted[i] = values.get(i);
        }
        return buildBalanced(sorted, 0, sorted.length - 1);
    }

    static TreeNode buildBalanced(long[] values, int lo, int hi) {
        if (lo > hi) {
            return null;
        }
        int mid = (lo + hi) / 2;
        TreeNode node = new TreeNode(values[mid]);
        node.left = buildBalanced(values, lo, mid - 1);
        node.right = buildBalanced(values, mid + 1, hi);
        return node;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
