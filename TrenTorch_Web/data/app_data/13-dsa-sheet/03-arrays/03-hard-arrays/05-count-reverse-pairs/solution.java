public class Main {
    // O(n log n) time, O(n) space
    static long countReversePairs(long[] nums) {
        if (nums == null || nums.length == 0) return 0;
        long[] arr = nums.clone();
        long[] temp = new long[arr.length];
        return mergeSortAndCount(arr, temp, 0, arr.length);
    }

    private static long mergeSortAndCount(long[] nums, long[] temp, int left, int right) {
        if (right - left <= 1) return 0;
        int mid = left + (right - left) / 2;
        long count = mergeSortAndCount(nums, temp, left, mid);
        count += mergeSortAndCount(nums, temp, mid, right);
        // Count cross reverse pairs
        int j = mid;
        for (int i = left; i < mid; i++) {
            while (j < right && nums[i] > 2 * nums[j]) {
                j++;
            }
            count += j - mid;
        }
        // Merge the two sorted halves
        int i = left, k = mid, idx = left;
        while (i < mid && k < right) {
            if (nums[i] <= nums[k]) {
                temp[idx++] = nums[i++];
            } else {
                temp[idx++] = nums[k++];
            }
        }
        while (i < mid) temp[idx++] = nums[i++];
        while (k < right) temp[idx++] = nums[k++];
        // Copy back to original array
        System.arraycopy(temp, left, nums, left, right - left);
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countReversePairs(new long[]{1L, 3L, 2L, 3L, 1L}));
    }
}
