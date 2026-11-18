// O(n log n) time, O(n) space
public class Main {
    static long countInversions(long[] nums) {
        if (nums == null || nums.length <= 1) return 0;
        long[] temp = new long[nums.length];
        return mergeSort(nums, temp, 0, nums.length - 1);
    }

    private static long mergeSort(long[] nums, long[] temp, int left, int right) {
        if (left >= right) return 0;
        int mid = left + (right - left) / 2;
        long count = mergeSort(nums, temp, left, mid);
        count += mergeSort(nums, temp, mid + 1, right);
        count += merge(nums, temp, left, mid, right);
        return count;
    }

    private static long merge(long[] nums, long[] temp, int left, int mid, int right) {
        for (int i = left; i <= right; i++) {
            temp[i] = nums[i];
        }
        int i = left;
        int j = mid + 1;
        int k = left;
        long cross = 0;
        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                nums[k++] = temp[i++];
            } else {
                nums[k++] = temp[j++];
                cross += (mid - i + 1);
            }
        }
        while (i <= mid) {
            nums[k++] = temp[i++];
        }
        while (j <= right) {
            nums[k++] = temp[j++];
        }
        return cross;
    }

    public static void main(String[] args) {
        System.out.println(countInversions(new long[]{3L, 1L, 2L}));
    }
}
