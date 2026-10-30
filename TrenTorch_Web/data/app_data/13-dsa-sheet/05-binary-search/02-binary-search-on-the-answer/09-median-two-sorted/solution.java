public class Main {
    // O(log(min(m, n))) time, O(1) space
    static double medianTwoSorted(long[] a, long[] b) {
        long[] A = a, B = b;
        if (A.length > B.length) {
            long[] tmp = A;
            A = B;
            B = tmp;
        }
        int m = A.length, n = B.length;
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            int i = (lo + hi) / 2;
            int j = half - i;
            double aLeft = i > 0 ? A[i - 1] : Double.NEGATIVE_INFINITY;
            double aRight = i < m ? A[i] : Double.POSITIVE_INFINITY;
            double bLeft = j > 0 ? B[j - 1] : Double.NEGATIVE_INFINITY;
            double bRight = j < n ? B[j] : Double.POSITIVE_INFINITY;
            if (aLeft <= bRight && bLeft <= aRight) {
                if ((m + n) % 2 == 1) {
                    return Math.max(aLeft, bLeft);
                }
                return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2.0;
            }
            if (aLeft > bRight) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }
        throw new IllegalArgumentException("inputs are not sorted");
    }

    public static void main(String[] args) {
        System.out.println(medianTwoSorted(new long[]{1L, 3L}, new long[]{2L}));
    }
}
