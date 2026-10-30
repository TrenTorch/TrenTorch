public class Main {
    // O(sqrt(n)) time, O(1) space
    static long sumDivisorCounts(long n) {
        long r = (long) Math.sqrt((double) n);
        while (r * r > n) {
            r--;
        }
        while ((r + 1) * (r + 1) <= n) {
            r++;
        }
        long sum = 0;
        for (long j = 1; j <= r; j++) {
            sum += n / j;
        }
        return 2 * sum - r * r;
    }

    public static void main(String[] args) {
        System.out.println(sumDivisorCounts(5L));
    }
}
