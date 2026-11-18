public class Main {
    // O(sqrt(n)) time, O(1) space
    static long eulerPhi(long n) {
        long result = n;
        long d = 2;
        while (d * d <= n) {
            if (n % d == 0) {
                while (n % d == 0) {
                    n /= d;
                }
                result -= result / d;
            }
            d += (d == 2) ? 1 : 2;
        }
        if (n > 1) {
            result -= result / n;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(eulerPhi(12L));
    }
}
