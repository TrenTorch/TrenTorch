public class Main {
    // O(n) time, O(1) space
    static long maxPoints(long[] points, long k) {
        int n = points.length;
        int size = n - (int) k;
        long window = 0;
        for (int i = 0; i < size; i++) {
            window += points[i];
        }
        long smallest = window;
        for (int i = size; i < n; i++) {
            window += points[i] - points[i - size];
            if (window < smallest) smallest = window;
        }
        long total = 0;
        for (long v : points) total += v;
        return total - smallest;
    }

    public static void main(String[] args) {
        System.out.println(maxPoints(new long[]{1L, 2L, 3L, 4L, 5L, 6L, 1L}, 3L));
    }
}
