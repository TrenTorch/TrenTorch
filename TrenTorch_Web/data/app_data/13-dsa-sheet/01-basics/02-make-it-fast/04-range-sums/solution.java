import java.util.Arrays;

public class Main {
    // O(n + q) time, O(n) space
    static long[] rangeSums(long[] nums, long[][] queries) {
        int n = nums.length;
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
        long[] ans = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int l = (int) queries[i][0];
            int r = (int) queries[i][1];
            ans[i] = prefix[r + 1] - prefix[l];
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(rangeSums(new long[]{1L, 2L, 3L, 4L, 5L}, new long[][]{new long[]{0L, 4L}, new long[]{1L, 3L}, new long[]{2L, 2L}})));
    }
}
