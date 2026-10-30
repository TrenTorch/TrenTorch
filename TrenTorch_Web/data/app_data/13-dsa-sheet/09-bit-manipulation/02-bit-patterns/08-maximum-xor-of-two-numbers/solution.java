public class Main {
    // O(30n) = O(n) time, O(n) space
    static long maxXorPair(long[] nums) {
        long best = 0;
        for (int bit = 29; bit >= 0; bit--) {
            java.util.HashSet<Long> prefixes = new java.util.HashSet<>();
            for (long x : nums) {
                prefixes.add(x >> bit);
            }
            long candidate = (best << 1) | 1L;
            best <<= 1;
            for (long p : prefixes) {
                if (prefixes.contains(p ^ candidate)) {
                    best = candidate;
                    break;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxXorPair(new long[]{3L, 10L, 5L, 25L, 2L, 8L}));
    }
}
