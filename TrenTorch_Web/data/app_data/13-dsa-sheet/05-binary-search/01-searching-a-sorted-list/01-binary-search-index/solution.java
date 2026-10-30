public class Main {
    // O(log n) time, O(1) space
    static long binarySearchIndex(long[] nums, long target) {
        int lo = 0;
        int hi = nums.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(binarySearchIndex(new long[]{-1L, 0L, 3L, 5L, 9L, 12L}, 9L));
    }
}
