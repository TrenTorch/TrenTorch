import java.util.Arrays;

public class Main {
    // O(n^2) time, O(1) space
    static long threeSumClosest(long[] nums, long target) {
        Arrays.sort(nums);
        long best = nums[0] + nums[1] + nums[2];
        int n = nums.length;
        for (int i = 0; i < n - 2; i++) {
            int lo = i + 1;
            int hi = n - 1;
            while (lo < hi) {
                long s = nums[i] + nums[lo] + nums[hi];
                long diff = Math.abs(s - target);
                long bestDiff = Math.abs(best - target);
                if (diff < bestDiff || (diff == bestDiff && s < best)) {
                    best = s;
                }
                if (s < target) {
                    lo++;
                } else if (s > target) {
                    hi--;
                } else {
                    return s;
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(threeSumClosest(new long[]{-1L, 2L, 1L, -4L}, 1L));
    }
}
