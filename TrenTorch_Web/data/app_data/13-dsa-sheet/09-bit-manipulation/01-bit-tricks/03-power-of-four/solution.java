public class Main {
    // O(1) time, O(1) space
    static boolean isPowerOfFour(long n) {
        return n > 0 && (n & (n - 1)) == 0 && (n & 0x5555555555555555L) != 0;
    }

    public static void main(String[] args) {
        System.out.println(isPowerOfFour(16L));
    }
}
