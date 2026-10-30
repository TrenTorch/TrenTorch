public class Main {
    // O(min(k, n - k)) time, O(1) space
    static long binomialMod(long n, long k) {
        final long mod = 1_000_000_007L;
        if (k < 0 || k > n) {
            return 0;
        }
        k = Math.min(k, n - k);
        long num = 1;
        long den = 1;
        for (long i = 0; i < k; i++) {
            num = num * ((n - i) % mod) % mod;
            den = den * (i + 1) % mod;
        }
        return num * powMod(den, mod - 2, mod) % mod;
    }

    static long powMod(long base, long exp, long mod) {
        long result = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1L) == 1L) {
                result = result * base % mod;
            }
            base = base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(binomialMod(5L, 2L));
    }
}
