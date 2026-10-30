import java.util.Collections;
import java.util.HashMap;

public class Main {
    // O(n^2 log C) time, O(n) space (C = coordinate range)
    static long maxPoints(long[][] points) {
        int n = points.length;
        if (n <= 2) {
            return n;
        }
        long best = 2;
        for (int i = 0; i < n; i++) {
            HashMap<Long, Integer> slopes = new HashMap<>();
            long x0 = points[i][0];
            long y0 = points[i][1];
            for (int j = i + 1; j < n; j++) {
                long dx = points[j][0] - x0;
                long dy = points[j][1] - y0;
                long g = gcd(Math.abs(dx), Math.abs(dy));
                dx /= g;
                dy /= g;
                if (dx < 0 || (dx == 0 && dy < 0)) {
                    dx = -dx;
                    dy = -dy;
                }
                slopes.merge(dx * 1_000_000L + dy, 1, Integer::sum);
            }
            if (!slopes.isEmpty()) {
                int most = Collections.max(slopes.values());
                best = Math.max(best, most + 1);
            }
        }
        return best;
    }

    static long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(maxPoints(new long[][]{new long[]{1L, 1L}, new long[]{2L, 2L}, new long[]{3L, 3L}}));
    }
}
