public class Main {
    // O(1) time, O(1) space
    static boolean isPowerOfTwo(long n) {
        return n > 0 && (n & (n - 1)) == 0;
    }

    public static void main(String[] args) {
        System.out.println(isPowerOfTwo(16L));
    }
}
