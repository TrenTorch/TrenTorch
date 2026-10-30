public class Main {
    // O(m log n) time, O(1) space
    static long nthRoot(long n, long m) {
        int bitLength = 64 - Long.numberOfLeadingZeros(n);
        long lo = 1;
        long hi = 1L << (bitLength / m + 1);

        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            long power = powLimit(mid, m, n);
            if (power == n) {
                return mid;
            } else if (power < n) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }

    private static long powLimit(long base, long exp, long limit) {
        long result = 1;
        for (int i = 0; i < exp; i++) {
            if (result > limit / base) {
                return limit + 1;
            }
            result *= base;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(nthRoot(27L, 3L));
    }
}
