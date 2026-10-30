class TreeNode {
    long val;
    TreeNode left, right;
    TreeNode(long val) { this.val = val; }
}

public class Main {
    // O(n) time, O(h) space
    static long largestBstSubtree(TreeNode root) {
        long[] best = {0};
        go(root, best);
        return best[0];
    }

    private static class Result {
        long size;
        long low;
        long high;
        Result(long size, long low, long high) {
            this.size = size;
            this.low = low;
            this.high = high;
        }
    }

    private static Result go(TreeNode node, long[] best) {
        if (node == null) {
            return new Result(0, Long.MAX_VALUE, Long.MIN_VALUE);
        }
        Result left = go(node.left, best);
        Result right = go(node.right, best);
        if (left.size >= 0 && right.size >= 0 && left.high < node.val && node.val < right.low) {
            long size = left.size + right.size + 1;
            if (size > best[0]) best[0] = size;
            long low = Math.min(left.low, node.val);
            long high = Math.max(right.high, node.val);
            return new Result(size, low, high);
        }
        return new Result(-1, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    public static void main(String[] args) {
        // Call it here and print the result to try it.
    }
}
