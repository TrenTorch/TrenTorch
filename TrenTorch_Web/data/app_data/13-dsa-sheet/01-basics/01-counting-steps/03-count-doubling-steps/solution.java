public class Main {
    // O(1) time, O(1) space
    static long countDoublingSteps(long n) {
        if (n <= 1) {
            return 0L;
        }
        return 64 - Long.numberOfLeadingZeros(n - 1);
    }

    public static void main(String[] args) {
        System.out.println(countDoublingSteps(8L));
    }
}
