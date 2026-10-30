public class Main {
    // O(2^n) time, O(2^n) space
    static long[] allSubsetSums(long[] nums) {
        long[] sums = new long[1];
        sums[0] = 0;
        for (long x : nums) {
            int n = sums.length;
            long[] newSums = new long[2 * n];
            int i = 0, j = 0, k = 0;
            while (i < n && j < n) {
                long val1 = sums[i];
                long val2 = sums[j] + x;
                if (val1 <= val2) {
                    newSums[k++] = val1;
                    i++;
                } else {
                    newSums[k++] = val2;
                    j++;
                }
            }
            while (i < n) {
                newSums[k++] = sums[i++];
            }
            while (j < n) {
                newSums[k++] = sums[j++] + x;
            }
            sums = newSums;
        }
        return sums;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(allSubsetSums(new long[]{1L, 2L})));
    }
}
