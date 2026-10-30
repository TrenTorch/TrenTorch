public class Main {
    // O(n) time, O(1) space
    static long countProductLess(long[] nums, long k) {
        long product = 1;
        int left = 0;
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            product *= nums[right];
            while (left <= right && product >= k) {
                product /= nums[left];
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countProductLess(new long[]{10L, 5L, 2L, 6L}, 100L));
    }
}
