public class Main {
    // O(1) time (fixed 32 bit positions), O(1) space
    static long longestOnesAfterFlip(long n) {
        long best = 0;
        long current = 0;
        long previous = 0;
        for (int i = 0; i < 32; i++) {
            if (((n >> i) & 1L) == 1L) {
                current++;
            } else {
                previous = current;
                current = 0;
            }
            best = Math.max(best, previous + current + 1);
        }
        return Math.min(best, 32);
    }

    public static void main(String[] args) {
        System.out.println(longestOnesAfterFlip(1775L));
    }
}
