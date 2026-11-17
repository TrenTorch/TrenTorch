import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    static long[] rearrangeBySign(long[] nums) {
        List<Long> pos = new ArrayList<>();
        List<Long> neg = new ArrayList<>();
        for (long x : nums) {
            if (x >= 0) {
                pos.add(x);
            } else {
                neg.add(x);
            }
        }
        long[] out = new long[nums.length];
        int idx = 0;
        int rounds = Math.max(pos.size(), neg.size());
        for (int i = 0; i < rounds; i++) {
            if (i < pos.size()) {
                out[idx++] = pos.get(i);
            }
            if (i < neg.size()) {
                out[idx++] = neg.get(i);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(rearrangeBySign(new long[]{3L, 1L, -2L, -5L, 2L, -4L})));
    }
}
