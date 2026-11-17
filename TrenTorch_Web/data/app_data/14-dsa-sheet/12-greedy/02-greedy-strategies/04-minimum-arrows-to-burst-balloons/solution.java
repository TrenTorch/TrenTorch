import java.util.Arrays;

public class Main {
    // O(n log n) time, O(n) space
    static long minArrows(long[][] points) {
        if (points == null || points.length == 0) return 0;
        Arrays.sort(points, (a, b) -> Long.compare(a[1], b[1]));
        long arrows = 0;
        long arrowPos = 0;
        boolean hasArrow = false;
        for (long[] p : points) {
            long start = p[0];
            long end = p[1];
            if (!hasArrow || start > arrowPos) {
                arrows++;
                arrowPos = end;
                hasArrow = true;
            }
        }
        return arrows;
    }

    public static void main(String[] args) {
        System.out.println(minArrows(new long[][]{new long[]{10L, 16L}, new long[]{2L, 8L}, new long[]{1L, 6L}, new long[]{7L, 12L}}));
    }
}
