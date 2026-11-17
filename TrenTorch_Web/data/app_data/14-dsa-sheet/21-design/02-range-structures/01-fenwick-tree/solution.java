import java.util.ArrayList;
import java.util.List;

public class Main {
    // O((n + q) log n) time, O(n) space
    static long[] runFenwick(long[] nums, String[] ops) {
        int n = nums.length;
        long[] tree = new long[n + 1];
        long[] values = nums.clone();
        for (int i = 0; i < n; i++) {
            fenwickAdd(tree, i, nums[i]);
        }
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("set")) {
                int i = Integer.parseInt(parts[1]);
                long v = Long.parseLong(parts[2]);
                fenwickAdd(tree, i, v - values[i]);
                values[i] = v;
            } else {
                int left = Integer.parseInt(parts[1]);
                int right = Integer.parseInt(parts[2]);
                out.add(fenwickPrefix(tree, right + 1) - fenwickPrefix(tree, left));
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    static void fenwickAdd(long[] tree, int i, long delta) {
        int n = tree.length - 1;
        i++;
        while (i <= n) {
            tree[i] += delta;
            i += i & -i;
        }
    }

    static long fenwickPrefix(long[] tree, int i) {
        long total = 0;
        while (i > 0) {
            total += tree[i];
            i -= i & -i;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runFenwick(new long[]{1L, 2L, 3L, 4L}, new String[]{"sum 0 3", "set 1 10", "sum 0 2", "sum 1 1"})));
    }
}
