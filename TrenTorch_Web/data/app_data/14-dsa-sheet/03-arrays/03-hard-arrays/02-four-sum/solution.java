import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n^3) time, O(n) extra space beyond the output (sort + two pointers)
    static long[][] fourSum(long[] nums, long target) {
        long[] a = nums.clone();
        Arrays.sort(a);
        int n = a.length;
        List<long[]> out = new ArrayList<>();
        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && a[i] == a[i - 1]) {
                continue;
            }
            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && a[j] == a[j - 1]) {
                    continue;
                }
                int lo = j + 1;
                int hi = n - 1;
                while (lo < hi) {
                    long total = a[i] + a[j] + a[lo] + a[hi];
                    if (total < target) {
                        lo++;
                    } else if (total > target) {
                        hi--;
                    } else {
                        out.add(new long[]{a[i], a[j], a[lo], a[hi]});
                        lo++;
                        hi--;
                        while (lo < hi && a[lo] == a[lo - 1]) {
                            lo++;
                        }
                        while (lo < hi && a[hi] == a[hi + 1]) {
                            hi--;
                        }
                    }
                }
            }
        }
        return out.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(Arrays.deepToString(fourSum(new long[]{1L, 0L, -1L, 0L, -2L, 2L}, 0L)));
    }
}
