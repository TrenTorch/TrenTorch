import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O((n + q) log n) time, O(n) space
    static long[] runSegmentTree(long[] nums, String[] ops) {
        int n = nums.length;
        long inf = Long.MAX_VALUE;
        long[] tree = new long[2 * n];
        Arrays.fill(tree, inf);
        for (int i = 0; i < n; i++) {
            tree[n + i] = nums[i];
        }
        for (int i = n - 1; i >= 1; i--) {
            tree[i] = Math.min(tree[2 * i], tree[2 * i + 1]);
        }
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("set")) {
                int i = Integer.parseInt(parts[1]) + n;
                tree[i] = Long.parseLong(parts[2]);
                i /= 2;
                while (i >= 1) {
                    tree[i] = Math.min(tree[2 * i], tree[2 * i + 1]);
                    i /= 2;
                }
            } else {
                int lo = Integer.parseInt(parts[1]) + n;
                int hi = Integer.parseInt(parts[2]) + n + 1;
                long best = inf;
                while (lo < hi) {
                    if ((lo & 1) == 1) {
                        best = Math.min(best, tree[lo]);
                        lo++;
                    }
                    if ((hi & 1) == 1) {
                        hi--;
                        best = Math.min(best, tree[hi]);
                    }
                    lo /= 2;
                    hi /= 2;
                }
                out.add(best);
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runSegmentTree(new long[]{5L, 2L, 8L, 1L}, new String[]{"min 0 3", "set 3 9", "min 0 3", "min 2 3"})));
    }
}
