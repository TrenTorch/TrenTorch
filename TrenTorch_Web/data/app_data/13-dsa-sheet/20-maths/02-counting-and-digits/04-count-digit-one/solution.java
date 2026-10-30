public class Main {
    // O(log n) time, O(1) space
    static long countDigitOne(long n) {
        long total = 0;
        long p = 1;
        while (p <= n) {
            long high = n / (p * 10);
            long cur = (n / p) % 10;
            long low = n % p;
            total += high * p;
            if (cur > 1) {
                total += p;
            } else if (cur == 1) {
                total += low + 1;
            }
            p *= 10;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countDigitOne(13L));
    }
}
