public class Main {
    // O(n) time, O(1) space
    static long josephus(long n, long k) {
        long position = 0;
        for (long m = 2; m <= n; m++) {
            position = (position + k) % m;
        }
        return position + 1;
    }

    public static void main(String[] args) {
        System.out.println(josephus(5L, 2L));
    }
}
