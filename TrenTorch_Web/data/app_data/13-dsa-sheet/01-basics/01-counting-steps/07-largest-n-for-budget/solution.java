import java.math.BigInteger;

public class Main {
    // O(log budget) time (binary search), O(1) space
    static long largestN(String growth, long budget) {
        if (growth.equals("2^n")) {
            return budget >= 2 ? 63 - Long.numberOfLeadingZeros(budget) : 0;
        }
        BigInteger limit = BigInteger.valueOf(budget);
        if (cost(growth, 1).compareTo(limit) > 0) {
            return 0;
        }
        long lo = 1;
        long hi = budget + 1;
        while (lo < hi) {
            long mid = lo + (hi - lo + 1) / 2;
            if (cost(growth, mid).compareTo(limit) <= 0) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        return lo;
    }

    // BigInteger so that n^3 cannot overflow during the search
    static BigInteger cost(String growth, long n) {
        BigInteger b = BigInteger.valueOf(n);
        if (growth.equals("n")) {
            return b;
        }
        if (growth.equals("n log n")) {
            return b.multiply(BigInteger.valueOf(63 - Long.numberOfLeadingZeros(n)));
        }
        if (growth.equals("n^2")) {
            return b.multiply(b);
        }
        return b.multiply(b).multiply(b);
    }

    public static void main(String[] args) {
        System.out.println(largestN("n^2", 100L));
    }
}
