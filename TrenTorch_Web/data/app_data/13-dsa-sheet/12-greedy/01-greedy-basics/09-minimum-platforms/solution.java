import java.util.Arrays;

public class Main {
    // O(n log n) time, O(1) space
    static long minPlatforms(long[] arrivals, long[] departures) {
        Arrays.sort(arrivals);
        Arrays.sort(departures);
        long current = 0;
        long best = 0;
        int i = 0;
        int j = 0;
        while (i < arrivals.length) {
            if (arrivals[i] <= departures[j]) {
                current++;
                if (current > best) best = current;
                i++;
            } else {
                current--;
                j++;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(minPlatforms(new long[]{900L, 940L, 950L, 1100L, 1500L, 1800L}, new long[]{910L, 1200L, 1120L, 1130L, 1900L, 2000L}));
    }
}
