import java.util.Arrays;

public class Main {
    // O(n) time, O(1) space (algebra on sums and sums of squares)
    static long[] repeatingAndMissing(long[] nums) {
        long n = nums.length;
        long sum = 0;
        long sumSquares = 0;
        for (long x : nums) {
            sum += x;
            sumSquares += x * x;
        }
        long diff = sum - n * (n + 1) / 2;                       // repeated - missing
        long squareDiff = sumSquares - n * (n + 1) * (2 * n + 1) / 6; // repeated^2 - missing^2
        long plus = squareDiff / diff;                            // repeated + missing (exact)
        return new long[]{(plus + diff) / 2, (plus - diff) / 2};
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(repeatingAndMissing(new long[]{3L, 1L, 2L, 5L, 3L})));
    }
}
