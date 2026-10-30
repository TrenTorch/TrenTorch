public class Main {
    // O(n) time, O(1) space
    static boolean checkSortedRotated(long[] nums) {
        int n = nums.length;
        int drops = 0;
        for (int i = 0; i < n; i++) {
            if (nums[i] > nums[(i + 1) % n]) {
                drops++;
                if (drops > 1) {
                    return false;
                }
            }
        }
        return drops <= 1;
    }

    public static void main(String[] args) {
        System.out.println(checkSortedRotated(new long[]{3L, 4L, 5L, 1L, 2L}));
    }
}
