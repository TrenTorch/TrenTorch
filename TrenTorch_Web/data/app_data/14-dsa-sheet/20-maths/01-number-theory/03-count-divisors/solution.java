public class Main {
    // O(sqrt(n)) time, O(1) space
    static long countDivisors(long n) {
        long count = 0;
        for (long d = 1; d * d <= n; d++) {
            if (n % d == 0) {
                count += (d * d == n) ? 1 : 2;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countDivisors(36L));
    }
}
