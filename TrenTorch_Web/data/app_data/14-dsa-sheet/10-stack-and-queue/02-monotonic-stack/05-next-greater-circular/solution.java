import java.util.Arrays;

public class Main {
    // O(n) time, O(n) space
    static long[] nextGreaterCircular(long[] nums) {
        int n = nums.length;
        long[] out = new long[n];
        Arrays.fill(out, -1);
        int[] stack = new int[n];
        int top = -1;
        for (int i = 0; i < 2 * n; i++) {
            long x = nums[i % n];
            while (top >= 0 && nums[stack[top]] < x) {
                out[stack[top]] = x;
                top--;
            }
            if (i < n) {
                stack[++top] = i;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(nextGreaterCircular(new long[]{1L, 2L, 1L})));
    }
}
