public class Main {
    // O(sqrt(n)) time, O(1) space
    static long countDivisorSteps(long n) {
        long total = 0;
        long i = 1;
        while (i <= n) {
            long q = n / i;
            long j = n / q;
            total += q * (j - i + 1);
            i = j + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countDivisorSteps(5L));
    }
}
