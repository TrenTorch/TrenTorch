public class Main {
    // O(n log n) time, O(n) space (sorted copy of the interval references)
    static long eraseOverlap(long[][] intervals) {
        long[][] sorted = intervals.clone();
        java.util.Arrays.sort(sorted, (a, b) -> Long.compare(a[1], b[1]));
        long removed = 0;
        Long lastEnd = null;
        for (long[] it : sorted) {
            long start = it[0];
            long end = it[1];
            if (lastEnd == null || start >= lastEnd) {
                lastEnd = end;
            } else {
                removed++;
            }
        }
        return removed;
    }

    public static void main(String[] args) {
        System.out.println(eraseOverlap(new long[][]{new long[]{1L, 2L}, new long[]{2L, 3L}, new long[]{3L, 4L}, new long[]{1L, 3L}}));
    }
}
