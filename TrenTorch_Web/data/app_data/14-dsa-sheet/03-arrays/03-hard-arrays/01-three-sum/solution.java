import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n^2) time, O(n) space
    static long[][] threeSum(long[] nums) {
        Arrays.sort(nums);
        List<long[]> res = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int lo = i + 1, hi = n - 1;
            while (lo < hi) {
                long total = nums[i] + nums[lo] + nums[hi];
                if (total < 0) {
                    lo++;
                } else if (total > 0) {
                    hi--;
                } else {
                    res.add(new long[]{nums[i], nums[lo], nums[hi]});
                    lo++;
                    hi--;
                    while (lo < hi && nums[lo] == nums[lo - 1]) lo++;
                    while (lo < hi && nums[hi] == nums[hi + 1]) hi--;
                }
            }
        }
        return res.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(threeSum(new long[]{-1L, 0L, 1L, 2L, -1L, -4L})));
    }
}
