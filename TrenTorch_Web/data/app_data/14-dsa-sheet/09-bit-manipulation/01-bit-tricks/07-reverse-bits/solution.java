public class Main {
    // O(1) time, O(1) space
    static long reverseBits(long n) {
        long result = 0;
        for (int i = 0; i < 32; i++) {
            result = (result << 1) | (n & 1);
            n >>>= 1;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(reverseBits(1L));
    }
}
