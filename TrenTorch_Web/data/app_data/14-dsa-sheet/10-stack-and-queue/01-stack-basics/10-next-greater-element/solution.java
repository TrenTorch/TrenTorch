public class Main {
    // O(n) time, O(n) space
    static long[] nextGreater(long[] nums) {
        long[] out = new long[nums.length];
        java.util.Arrays.fill(out, -1L);
        int[] stack = new int[nums.length];
        int top = 0;
        for (int i = 0; i < nums.length; i++) {
            long x = nums[i];
            while (top > 0 && nums[stack[top - 1]] < x) {
                out[stack[--top]] = x;
            }
            stack[top++] = i;
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(nextGreater(new long[]{2L, 1L, 2L, 4L, 3L})));
    }
}
