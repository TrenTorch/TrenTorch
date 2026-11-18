public class Main {
    // O(1) time, O(1) space
    static long andOfRange(long left, long right) {
        long x = left ^ right;
        int shift = 64 - Long.numberOfLeadingZeros(x);
        return (left >> shift) << shift;
    }

    public static void main(String[] args) {
        System.out.println(andOfRange(5L, 7L));
    }
}
