public class Main {
    // O(log n) time, O(1) space
    static long[] firstAndLast(long[] nums, long target) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if (lo == nums.length || nums[lo] != target) {
            return new long[]{-1, -1};
        }
        int first = lo;
        hi = nums.length;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (nums[mid] <= target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return new long[]{first, lo - 1};
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(firstAndLast(new long[]{5L, 7L, 7L, 8L, 8L, 10L}, 8L)));
    }
}
