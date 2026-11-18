import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n log n) time and space to build, O(1) time per query
    static long[] rangeMinimums(long[] nums, long[][] queries) {
        int n = nums.length;
        List<long[]> table = new ArrayList<>();
        table.add(nums.clone());
        for (int k = 1; (1 << k) <= n; k++) {
            long[] prev = table.get(k - 1);
            int half = 1 << (k - 1);
            long[] cur = new long[prev.length - half];
            for (int i = 0; i < cur.length; i++) {
                cur[i] = Math.min(prev[i], prev[i + half]);
            }
            table.add(cur);
        }
        long[] out = new long[queries.length];
        for (int q = 0; q < queries.length; q++) {
            int left = (int) queries[q][0];
            int right = (int) queries[q][1];
            int len = right - left + 1;
            int level = 31 - Integer.numberOfLeadingZeros(len);
            long[] row = table.get(level);
            out[q] = Math.min(row[left], row[right - (1 << level) + 1]);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(rangeMinimums(new long[]{5L, 2L, 8L, 1L, 9L}, new long[][]{new long[]{0L, 4L}, new long[]{1L, 2L}, new long[]{2L, 2L}})));
    }
}
