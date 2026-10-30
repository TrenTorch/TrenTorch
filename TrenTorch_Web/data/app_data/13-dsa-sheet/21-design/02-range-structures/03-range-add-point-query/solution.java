import java.util.ArrayList;
import java.util.List;

public class Main {
    // O((n + q) log n) time, O(n) space
    static long[] runRangeAdd(long n, String[] ops) {
        int size = (int) n;
        long[] tree = new long[size + 2];
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("add")) {
                int left = Integer.parseInt(parts[1]);
                int right = Integer.parseInt(parts[2]);
                long v = Long.parseLong(parts[3]);
                rangeAddUpdate(tree, left, v);
                rangeAddUpdate(tree, right + 1, -v);
            } else {
                out.add(rangeAddPrefix(tree, Integer.parseInt(parts[1])));
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    static void rangeAddUpdate(long[] tree, int i, long delta) {
        int limit = tree.length - 1;
        i++;
        while (i <= limit) {
            tree[i] += delta;
            i += i & -i;
        }
    }

    static long rangeAddPrefix(long[] tree, int i) {
        long total = 0;
        i++;
        while (i > 0) {
            total += tree[i];
            i -= i & -i;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runRangeAdd(5L, new String[]{"add 1 3 10", "get 2", "add 0 4 -1", "get 0", "get 3"})));
    }
}
