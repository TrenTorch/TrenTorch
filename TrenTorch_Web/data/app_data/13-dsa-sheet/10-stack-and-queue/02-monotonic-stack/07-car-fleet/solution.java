import java.util.Arrays;

public class Main {
    // O(n log n) time, O(n) space
    static long carFleet(long target, long[][] cars) {
        if (cars == null || cars.length == 0) {
            return 0;
        }
        Arrays.sort(cars, (a, b) -> Long.compare(b[0], a[0]));
        long fleets = 0;
        long slowNum = 0;
        long slowDen = 1;
        for (long[] car : cars) {
            long pos = car[0];
            long spd = car[1];
            long num = target - pos;
            long den = spd;
            if (num * slowDen > slowNum * den) {
                fleets++;
                slowNum = num;
                slowDen = den;
            }
        }
        return fleets;
    }

    public static void main(String[] args) {
        System.out.println(carFleet(12L, new long[][]{new long[]{10L, 2L}, new long[]{8L, 4L}, new long[]{0L, 1L}, new long[]{5L, 1L}, new long[]{3L, 3L}}));
    }
}
