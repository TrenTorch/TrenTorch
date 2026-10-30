import java.util.Arrays;

public class Main {
    // O(n log n + n log(max - min)) time, O(n) space for the sorted copy
    static long aggressiveCows(long[] stalls, long cows) {
        long[] s = stalls.clone();
        Arrays.sort(s);
        long lo = 1, hi = s[s.length - 1] - s[0];
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            if (canPlace(s, mid, cows)) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        return lo;
    }

    static boolean canPlace(long[] s, long distance, long cows) {
        long placed = 1, last = s[0];
        for (int i = 1; i < s.length; i++) {
            if (s[i] - last >= distance) {
                placed++;
                last = s[i];
            }
        }
        return placed >= cows;
    }

    public static void main(String[] args) {
        System.out.println(aggressiveCows(new long[]{1L, 2L, 4L, 8L, 9L}, 3L));
    }
}
