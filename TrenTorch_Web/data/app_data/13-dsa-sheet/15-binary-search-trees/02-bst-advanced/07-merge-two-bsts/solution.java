import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n+m) time, O(n+m) space
    static long[] mergeBsts(TreeNode root1, TreeNode root2) {
        List<Long> list1 = inorder(root1);
        List<Long> list2 = inorder(root2);
        long[] result = new long[list1.size() + list2.size()];
        int i = 0, j = 0, k = 0;
        while (i < list1.size() && j < list2.size()) {
            if (list1.get(i) <= list2.get(j)) {
                result[k++] = list1.get(i++);
            } else {
                result[k++] = list2.get(j++);
            }
        }
        while (i < list1.size()) {
            result[k++] = list1.get(i++);
        }
        while (j < list2.size()) {
            result[k++] = list2.get(j++);
        }
        return result;
    }

    private static List<Long> inorder(TreeNode root) {
        List<Long> out = new ArrayList<>();
        Stack<TreeNode> stack = new Stack<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
            node = stack.pop();
            out.add(node.val);
            node = node.right;
        }
        return out;
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
