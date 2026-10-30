import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class Main {
    // O(n log n) time, O(n) space
    static long[][] mergeIntervals(long[][] intervals) {
        if (intervals == null || intervals.length == 0) {
            return new long[0][];
        }
        Arrays.sort(intervals, Comparator.comparingLong(a -> a[0]));
        ArrayList<long[]> merged = new ArrayList<>();
        for (long[] interval : intervals) {
            long start = interval[0];
            long end = interval[1];
            if (!merged.isEmpty() && start <= merged.get(merged.size() - 1)[1]) {
                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], end);
            } else {
                merged.add(new long[]{start, end});
            }
        }
        return merged.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(mergeIntervals(new long[][]{new long[]{1L, 3L}, new long[]{8L, 10L}, new long[]{2L, 6L}, new long[]{15L, 18L}})));
    }
}
