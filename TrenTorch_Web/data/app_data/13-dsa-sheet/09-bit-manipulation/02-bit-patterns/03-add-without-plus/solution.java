public class Main {
    // O(1) time (at most 32 carry rounds), O(1) space
    static long bitAdd(long a, long b) {
        long mask = 0xFFFFFFFFL;
        a &= mask;
        b &= mask;
        while (b != 0) {
            long carry = ((a & b) << 1) & mask;
            a = (a ^ b) & mask;
            b = carry;
        }
        return a >= (1L << 31) ? a - (1L << 32) : a;
    }

    public static void main(String[] args) {
        System.out.println(bitAdd(1L, 2L));
    }
}
