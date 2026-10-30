public class Main {
    // O(n * target / 64) time, O(target / 64) space (bitset of reachable sums)
    static boolean subsetSum(long[] nums, long target) {
        int t = (int) target;
        long[] bits = new long[(t >>> 6) + 1];
        bits[0] = 1L;
        for (long x : nums) {
            shiftOr(bits, (int) x);
        }
        return ((bits[t >>> 6] >>> (t & 63)) & 1L) == 1L;
    }

    // bits |= bits << x, done in place from high words to low words;
    // bit k set means sum k is reachable
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
        System.out.println(subsetSum(new long[]{3L, 34L, 4L, 12L, 5L, 2L}, 9L));
    }
}
