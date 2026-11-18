public class Main {
    // O(n log n) time, O(n) space
    static long maxActivities(long[] starts, long[] ends) {
        long[][] pairs = new long[starts.length][];
        for (int i = 0; i < starts.length; i++) {
            pairs[i] = new long[]{ends[i], starts[i]};
        }
        java.util.Arrays.sort(pairs, (a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        long count = 0;
        long lastEnd = -1;
        for (long[] p : pairs) {
            long end = p[0];
            long start = p[1];
            if (start >= lastEnd) {
                count++;
                lastEnd = end;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(maxActivities(new long[]{1L, 3L, 0L, 5L, 8L, 5L}, new long[]{2L, 4L, 6L, 7L, 9L, 9L}));
    }
}
