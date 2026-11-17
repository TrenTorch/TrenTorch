import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] arrayLeaders(long[] nums) {
        long[] fromRight = new long[nums.length];
        int count = 0;
        boolean hasBest = false;
        long best = 0;
        for (int i = nums.length - 1; i >= 0; i--) {
            if (!hasBest || nums[i] > best) {
                fromRight[count++] = nums[i];
                best = nums[i];
                hasBest = true;
            }
        }
        long[] out = new long[count];
        for (int j = 0; j < count; j++) {
            out[j] = fromRight[count - 1 - j];
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(arrayLeaders(new long[]{16L, 17L, 4L, 3L, 5L, 2L})));
    }
}
