public class Main {
    // O(log(min(m, n))) time, O(1) space
    static long kthOfTwoSorted(long[] a, long[] b, long k) {
        long[] A = a, B = b;
        if (A.length > B.length) {
            long[] tmp = A;
            A = B;
            B = tmp;
        }
        int m = A.length, n = B.length;
        int K = (int) k;
        int lo = Math.max(0, K - n), hi = Math.min(K, m);
        while (lo <= hi) {
            int i = (lo + hi) / 2;
            int j = K - i;
            double aLeft = i > 0 ? A[i - 1] : Double.NEGATIVE_INFINITY;
            double aRight = i < m ? A[i] : Double.POSITIVE_INFINITY;
            double bLeft = j > 0 ? B[j - 1] : Double.NEGATIVE_INFINITY;
            double bRight = j < n ? B[j] : Double.POSITIVE_INFINITY;
            if (aLeft <= bRight && bLeft <= aRight) {
                return (long) Math.max(aLeft, bLeft);
            }
            if (aLeft > bRight) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }
        throw new IllegalArgumentException("inputs are not sorted or k is out of range");
    }

    public static void main(String[] args) {
        System.out.println(kthOfTwoSorted(new long[]{2L, 3L, 6L, 7L, 9L}, new long[]{1L, 4L, 8L, 10L}, 5L));
    }
}
