public class Main {
    // O(log_5 n) time, O(1) space (count factors of 5 in n!)
    static long trailingZeros(long n) {
        long count = 0;
        while (n > 0) {
            n /= 5;
            count += n;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(trailingZeros(25L));
    }
}
