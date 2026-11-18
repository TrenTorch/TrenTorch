public class Main {
    // O(log exp) time, O(1) space (binary exponentiation)
    static long powerMod(long base, long exp, long mod) {
        long result = 1 % mod;
        base %= mod;
        while (exp != 0) {
            if ((exp & 1) == 1) {
                result = result * base % mod;
            }
            base = base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(powerMod(2L, 10L, 1000L));
    }
}
