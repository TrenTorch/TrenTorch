public class Main {
    // O(n) time, O(n) space
    static long[] countBitsUpTo(long n) {
        int size = (int) n + 1;
        long[] bits = new long[size];
        for (long i = 1; i <= n; i++) {
            bits[(int) i] = bits[(int) (i >> 1)] + (i & 1);
        }
        return bits;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(countBitsUpTo(5L)));
    }
}
