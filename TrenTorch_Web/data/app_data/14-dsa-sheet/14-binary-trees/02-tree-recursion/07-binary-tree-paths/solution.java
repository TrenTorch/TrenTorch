import java.util.ArrayList;
import java.util.List;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(n) space
    static String[] rootToLeafPaths(TreeNode root) {
        List<String> result = new ArrayList<>();
        List<String> path = new ArrayList<>();
        dfs(root, path, result);
        return result.toArray(new String[0]);
    }

    private static void dfs(TreeNode node, List<String> path, List<String> result) {
        if (node == null) {
            return;
        }
        path.add(String.valueOf(node.val));
        if (node.left == null && node.right == null) {
            result.add(String.join("->", path));
        } else {
            dfs(node.left, path, result);
            dfs(node.right, path, result);
        }
        path.remove(path.size() - 1);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
