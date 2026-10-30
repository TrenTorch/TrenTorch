public class Main {
    // O(n) time, O(n) space for the copy
    static long[] keepAtMostTwice(long[] nums) {
        long[] a = nums.clone();
        int write = 0;
        for (int read = 0; read < a.length; read++) {
            if (write < 2 || a[read] != a[write - 2]) {
                a[write] = a[read];
                write++;
            }
        }
        return java.util.Arrays.copyOf(a, write);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(keepAtMostTwice(new long[]{1L, 1L, 1L, 2L, 2L, 3L})));
    }
}
