public class Main {
    // O(log n) time, O(1) space
    static long countOccurrences(long[] nums, long target) {
        int left = lowerBound(nums, target);
        int right = upperBound(nums, target);
        return right - left;
    }

    private static int lowerBound(long[] nums, long target) {
        int low = 0, high = nums.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] < target) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low;
    }

    private static int upperBound(long[] nums, long target) {
        int low = 0, high = nums.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] <= target) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low;
    }

    public static void main(String[] args) {
        System.out.println(countOccurrences(new long[]{1L, 2L, 2L, 2L, 3L}, 2L));
    }
}
