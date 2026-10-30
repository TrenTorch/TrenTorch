import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static long[] distanceK(TreeNode root, long target, long k) {
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        TreeNode targetNode = null;
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        parent.put(root, null);

        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            if (node.val == target) {
                targetNode = node;
            }
            if (node.right != null) {
                parent.put(node.right, node);
                stack.push(node.right);
            }
            if (node.left != null) {
                parent.put(node.left, node);
                stack.push(node.left);
            }
        }

        Set<TreeNode> seen = new HashSet<>();
        Deque<TreeNode> queue = new ArrayDeque<>();
        seen.add(targetNode);
        queue.add(targetNode);

        for (long i = 0; i < k; i++) {
            int size = queue.size();
            for (int j = 0; j < size; j++) {
                TreeNode node = queue.poll();
                if (node.left != null && !seen.contains(node.left)) {
                    seen.add(node.left);
                    queue.add(node.left);
                }
                if (node.right != null && !seen.contains(node.right)) {
                    seen.add(node.right);
                    queue.add(node.right);
                }
                TreeNode par = parent.get(node);
                if (par != null && !seen.contains(par)) {
                    seen.add(par);
                    queue.add(par);
                }
            }
        }

        List<Long> result = new ArrayList<>();
        for (TreeNode node : queue) {
            result.add(node.val);
        }
        Collections.sort(result);
        long[] ans = new long[result.size()];
        for (int i = 0; i < result.size(); i++) {
            ans[i] = result.get(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
