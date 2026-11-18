import java.util.*;

class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n log n) time, O(n) space
    static long[][] verticalOrder(TreeNode root) {
        if (root == null) {
            return new long[0][];
        }
        Map<Integer, List<long[]>> columns = new TreeMap<>();
        Queue<Entry> queue = new ArrayDeque<>();
        queue.offer(new Entry(root, 0, 0));
        while (!queue.isEmpty()) {
            Entry e = queue.poll();
            TreeNode node = e.node;
            int row = e.row;
            int col = e.col;
            columns.computeIfAbsent(col, k -> new ArrayList<>()).add(new long[]{row, node.val});
            if (node.left != null) {
                queue.offer(new Entry(node.left, row + 1, col - 1));
            }
            if (node.right != null) {
                queue.offer(new Entry(node.right, row + 1, col + 1));
            }
        }
        long[][] result = new long[columns.size()][];
        int idx = 0;
        for (List<long[]> list : columns.values()) {
            list.sort((a, b) -> {
                if (a[0] != b[0]) {
                    return Long.compare(a[0], b[0]);
                }
                return Long.compare(a[1], b[1]);
            });
            long[] colVals = new long[list.size()];
            for (int i = 0; i < list.size(); i++) {
                colVals[i] = list.get(i)[1];
            }
            result[idx++] = colVals;
        }
        return result;
    }

    static class Entry {
        TreeNode node;
        int row;
        int col;
        Entry(TreeNode node, int row, int col) {
            this.node = node;
            this.row = row;
            this.col = col;
        }
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
