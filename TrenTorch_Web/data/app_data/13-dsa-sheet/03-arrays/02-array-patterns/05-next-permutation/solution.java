public class Main {
    // O(n) time, O(n) space
    static long[] nextPermutation(long[] nums) {
        long[] a = nums.clone();
        int i = a.length - 2;
        while (i >= 0 && a[i] >= a[i + 1]) {
            i--;
        }
        if (i >= 0) {
            int j = a.length - 1;
            while (a[j] <= a[i]) {
                j--;
            }
            long tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
        // reverse a[i+1 .. end]
        int left = i + 1;
        int right = a.length - 1;
        while (left < right) {
            long tmp = a[left];
            a[left] = a[right];
            a[right] = tmp;
            left++;
            right--;
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(nextPermutation(new long[]{1L, 2L, 3L})));
    }
}
