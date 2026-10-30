import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayDeque;
import java.util.Map;
import java.util.Set;
import java.util.Deque;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long burnTime(TreeNode root, long start) {
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        TreeNode origin = null;
        Deque<TreeNode[]> stack = new ArrayDeque<>();
        stack.push(new TreeNode[]{root, null});
        while (!stack.isEmpty()) {
            TreeNode[] pair = stack.pop();
            TreeNode node = pair[0];
            TreeNode par = pair[1];
            parent.put(node, par);
            if (node.val == start) {
                origin = node;
            }
            if (node.right != null) {
                stack.push(new TreeNode[]{node.right, node});
            }
            if (node.left != null) {
                stack.push(new TreeNode[]{node.left, node});
            }
        }
        Set<TreeNode> seen = new HashSet<>();
        Deque<TreeNode> frontier = new ArrayDeque<>();
        seen.add(origin);
        frontier.add(origin);
        int minutes = -1;
        while (!frontier.isEmpty()) {
            minutes++;
            int size = frontier.size();
            for (int i = 0; i < size; i++) {
                TreeNode node = frontier.poll();
                TreeNode left = node.left;
                TreeNode right = node.right;
                TreeNode par = parent.get(node);
                if (left != null && !seen.contains(left)) {
                    seen.add(left);
                    frontier.add(left);
                }
                if (right != null && !seen.contains(right)) {
                    seen.add(right);
                    frontier.add(right);
                }
                if (par != null && !seen.contains(par)) {
                    seen.add(par);
                    frontier.add(par);
                }
            }
        }
        return minutes;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
