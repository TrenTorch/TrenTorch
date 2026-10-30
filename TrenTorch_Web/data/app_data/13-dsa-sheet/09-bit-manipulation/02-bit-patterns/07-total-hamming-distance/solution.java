public class Main {
    // O(30n) = O(n) time, O(1) space
    static long totalHammingDistance(long[] nums) {
        long n = nums.length;
        long total = 0;
        for (int i = 0; i < 30; i++) {
            long ones = 0;
            for (long x : nums) {
                ones += (x >> i) & 1L;
            }
            total += ones * (n - ones);
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(totalHammingDistance(new long[]{4L, 14L, 2L}));
    }
}
