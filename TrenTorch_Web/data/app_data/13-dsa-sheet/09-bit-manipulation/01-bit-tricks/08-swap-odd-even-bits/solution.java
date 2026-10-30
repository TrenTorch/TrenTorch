public class Main {
    // O(1) time, O(1) space
    static long swapOddEvenBits(long n) {
        long evenMask = 0x55555555L; // bits at even positions (0,2,4,...)
        long oddMask = 0xAAAAAAAAL;  // bits at odd positions (1,3,5,...)
        return ((n & evenMask) << 1) | ((n & oddMask) >>> 1);
    }

    public static void main(String[] args) {
        System.out.println(swapOddEvenBits(10L));
    }
}
