public class Main {
    static final long MOD = 1000000007L;

    // O(min(rows, cols) * log MOD) time, O(1) space
    static long uniquePaths(long rows, long cols) {
        long n = rows + cols - 2;
        long k = rows - 1;
        if (k > n - k) k = n - k;
        long ans = 1;
        for (long i = 1; i <= k; i++) {
            ans = ans * (n - k + i) % MOD;
            ans = ans * modPow(i, MOD - 2) % MOD;
        }
        return ans;
    }

    static long modPow(long a, long e) {
        long res = 1;
        a %= MOD;
        while (e > 0) {
            if ((e & 1) == 1) res = res * a % MOD;
            a = a * a % MOD;
            e >>= 1;
        }
        return res;
    }

    public static void main(String[] args) {
        System.out.println(uniquePaths(3L, 7L));
    }
}
