public class Main {
    static final long MOD = 1_000_000_007L;

    // O(log n) time, O(log n) space (recursion depth)
    static long climbStairs(long n) {
        return fib(n + 1)[0];
    }

    // returns {F(k), F(k + 1)} modulo MOD
    static long[] fib(long k) {
        if (k == 0) {
            return new long[]{0L, 1L};
        }
        long[] half = fib(k >> 1);
        long a = half[0];
        long b = half[1];
        long t = ((2 * b - a) % MOD + MOD) % MOD;
        long c = a * t % MOD;
        long d = (a * a + b * b) % MOD;
        return (k & 1) == 1 ? new long[]{d, (c + d) % MOD} : new long[]{c, d};
    }

    public static void main(String[] args) {
        System.out.println(climbStairs(3L));
    }
}
