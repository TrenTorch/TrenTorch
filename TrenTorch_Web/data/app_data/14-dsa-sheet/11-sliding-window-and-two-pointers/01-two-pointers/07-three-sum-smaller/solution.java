public class Main {
    // O(n^2) time (sort plus two pointers), O(n) space for the sorted copy
    static long countTripletsSmaller(long[] nums, long target) {
        long[] a = nums.clone();
        java.util.Arrays.sort(a);
        long count = 0;
        for (int i = 0; i + 2 < a.length; i++) {
            int lo = i + 1;
            int hi = a.length - 1;
            while (lo < hi) {
                if (a[i] + a[lo] + a[hi] < target) {
                    count += hi - lo;
                    lo++;
                } else {
                    hi--;
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countTripletsSmaller(new long[]{-2L, 0L, 1L, 3L}, 2L));
    }
}
