public class Main {
    // O(n) time, O(1) space
    static long findDuplicate(long[] nums) {
        long slow = nums[0];
        long fast = nums[0];
        while (true) {
            slow = nums[(int) slow];
            fast = nums[(int) nums[(int) fast]];
            if (slow == fast) {
                break;
            }
        }
        slow = nums[0];
        while (slow != fast) {
            slow = nums[(int) slow];
            fast = nums[(int) fast];
        }
        return slow;
    }

    public static void main(String[] args) {
        System.out.println(findDuplicate(new long[]{1L, 3L, 4L, 2L, 2L}));
    }
}
