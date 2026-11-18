public class Main {
    // O(n log M) time, O(1) space where n = number of congruences, M = max modulus
    static long solveCongruences(long[] remainders, long[] moduli) {
        long x = 0;
        long modulus = 1;
        for (int i = 0; i < remainders.length; i++) {
            long r = remainders[i];
            long m = moduli[i];
            long g = gcd(modulus, m);
            if ((r - x) % g != 0) {
                return -1;
            }
            long lcm = modulus / g * m;
            long diff = (r - x) / g;
            long a = modulus / g;
            long mod = m / g;
            long inv = modInverse(a, mod);
            long t = (diff * inv) % mod;
            if (t < 0) t += mod;
            x = (x + modulus * t) % lcm;
            if (x < 0) x += lcm;
            modulus = lcm;
        }
        return x;
    }

    static long gcd(long a, long b) {
        while (b != 0) {
            long t = b;
            b = a % b;
            a = t;
        }
        return a;
    }

    // returns inverse of a modulo mod, assuming gcd(a, mod) == 1
    static long modInverse(long a, long mod) {
        long m0 = mod;
        long y = 0, x = 1;
        if (mod == 1) return 0;
        while (a > 1) {
            long q = a / mod;
            long t = mod;
            mod = a % mod;
            a = t;
            t = y;
            y = x - q * y;
            x = t;
        }
        if (x < 0) x += m0;
        return x;
    }

    public static void main(String[] args) {
        System.out.println(solveCongruences(new long[]{2L, 3L, 2L}, new long[]{3L, 5L, 7L}));
    }
}
