public class Main {
    // O(len(b)) time, O(1) space
    static long superPow(long a, long[] b) {
        final long mod = 1337L;
        long result = 1;
        for (long digit : b) {
            result = powMod(result, 10, mod) * powMod(a, digit, mod) % mod;
        }
        return result;
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
        System.out.println(superPow(2L, new long[]{1L, 0L}));
    }
}
