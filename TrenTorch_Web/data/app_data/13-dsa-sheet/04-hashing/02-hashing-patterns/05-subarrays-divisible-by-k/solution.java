public class Main {
    // O(n) time, O(k) space
    static long subarraysDivisibleByK(long[] nums, long k) {
        int K = (int) k;
        long[] count = new long[K];
        count[0] = 1;
        long prefix = 0;
        long ans = 0;
        for (long x : nums) {
            prefix = (prefix + x) % K;
            if (prefix < 0) prefix += K;
            ans += count[(int) prefix];
            count[(int) prefix]++;
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(subarraysDivisibleByK(new long[]{4L, 5L, 0L, -2L, -3L, 1L}, 5L));
    }
}
