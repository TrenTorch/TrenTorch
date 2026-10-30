public class Main {
    // O(n * total / 64) time, O(total / 64) space (bitset of reachable sums)
    static long minSubsetDifference(long[] nums) {
        long total = 0;
        for (long x : nums) {
            total += x;
        }
        int t = (int) total;
        long[] bits = new long[(t >>> 6) + 1];
        bits[0] = 1L;
        for (long x : nums) {
            shiftOr(bits, (int) x);
        }
        for (int s = t / 2; s >= 0; s--) {
            if (((bits[s >>> 6] >>> (s & 63)) & 1L) == 1L) {
                return total - 2L * s;
            }
        }
        return total;
    }

    // bits |= bits << x, done in place from high words to low words
    static void shiftOr(long[] bits, int x) {
        int words = x >>> 6;
        int shift = x & 63;
        for (int i = bits.length - 1; i >= words; i--) {
            int src = i - words;
            long moved = bits[src] << shift;
            if (shift != 0 && src - 1 >= 0) {
                moved |= bits[src - 1] >>> (64 - shift);
            }
            bits[i] |= moved;
        }
    }

    public static void main(String[] args) {
        System.out.println(minSubsetDifference(new long[]{1L, 6L, 11L, 5L}));
    }
}
