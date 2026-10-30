import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    // O(n) time, O(1) space
    static long[] majorityElementThirds(long[] nums) {
        if (nums == null || nums.length == 0) {
            return new long[0];
        }
        long a = 0, b = 0;
        int ca = 0, cb = 0;
        for (long x : nums) {
            if (x == a) {
                ca++;
            } else if (x == b) {
                cb++;
            } else if (ca == 0) {
                a = x;
                ca = 1;
            } else if (cb == 0) {
                b = x;
                cb = 1;
            } else {
                ca--;
                cb--;
            }
        }
        long countA = 0, countB = 0;
        for (long x : nums) {
            if (x == a) {
                countA++;
            } else if (x == b) {
                countB++;
            }
        }
        List<Long> result = new ArrayList<>();
        int n = nums.length;
        if (countA * 3 > n) {
            result.add(a);
        }
        if (b != a && countB * 3 > n) {
            result.add(b);
        }
        Collections.sort(result);
        long[] res = new long[result.size()];
        for (int i = 0; i < res.length; i++) {
            res[i] = result.get(i);
        }
        return res;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(majorityElementThirds(new long[]{3L, 2L, 3L})));
    }
}
