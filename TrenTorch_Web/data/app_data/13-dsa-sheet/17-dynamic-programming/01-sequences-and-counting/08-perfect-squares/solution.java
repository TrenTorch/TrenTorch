public class Main {
    // O(sqrt(n)) time, O(1) space
    static long numSquares(long n) {
        if (n == 0) {
            return 0;
        }
        long sqrtN = (long) Math.sqrt(n);
        if (sqrtN * sqrtN == n) {
            return 1;
        }
        long m = n;
        while (m % 4 == 0) {
            m /= 4;
        }
        if (m % 8 == 7) {
            return 4;
        }
        for (long i = 1; i * i <= n; i++) {
            long rest = n - i * i;
            long sqrtRest = (long) Math.sqrt(rest);
            if (sqrtRest * sqrtRest == rest) {
                return 2;
            }
        }
        return 3;
    }

    public static void main(String[] args) {
        System.out.println(numSquares(12L));
    }
}
