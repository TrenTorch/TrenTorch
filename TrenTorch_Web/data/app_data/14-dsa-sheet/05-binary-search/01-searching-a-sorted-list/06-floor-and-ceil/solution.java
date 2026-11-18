public class Main {
    // O(log n) time, O(1) space
    static long[] floorAndCeil(long[] nums, long target) {
        int lo = 0;
        int hi = nums.length;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (nums[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        long ceil = (lo < nums.length) ? nums[lo] : -1;
        long floor;
        if (lo < nums.length && nums[lo] == target) {
            floor = target;
        } else {
            floor = (lo > 0) ? nums[lo - 1] : -1;
        }
        return new long[]{floor, ceil};
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(floorAndCeil(new long[]{1L, 2L, 8L, 10L, 11L, 12L, 19L}, 5L)));
    }
}
