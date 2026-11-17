public class Main {
    static final long MOD = 1_000_000_007L;

    // O(log n) time, O(log n) space (fast doubling with recursion)
    static long fibMod(long n) {
        return pair(n)[0];
    }

    // Returns {F(k) mod MOD, F(k+1) mod MOD}
    static long[] pair(long k) {
        if (k == 0) {
            return new long[]{0, 1};
        }
        long[] p = pair(k / 2);
        long a = p[0];
        long b = p[1];
        long c = a * (((2 * b - a) % MOD + MOD) % MOD) % MOD;
        long e = (a * a + b * b) % MOD;
        if (k % 2 == 1) {
            return new long[]{e, (c + e) % MOD};
        }
        return new long[]{c, e};
    }

    public static void main(String[] args) {
        System.out.println(fibMod(10L));
    }
}
