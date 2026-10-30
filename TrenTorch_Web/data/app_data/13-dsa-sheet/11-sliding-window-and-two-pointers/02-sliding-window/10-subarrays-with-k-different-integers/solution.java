public class Main {
    // O(n) time, O(n) space (window map of distinct values)
    static long subarraysKDistinct(long[] nums, long k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private static long atMost(long[] nums, long m) {
        java.util.Map<Long, Integer> count = new java.util.HashMap<>();
        int left = 0;
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            count.merge(nums[right], 1, Integer::sum);
            while (count.size() > m) {
                long x = nums[left];
                int c = count.get(x) - 1;
                if (c == 0) {
                    count.remove(x);
                } else {
                    count.put(x, c);
                }
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(subarraysKDistinct(new long[]{1L, 2L, 1L, 2L, 3L}, 2L));
    }
}
