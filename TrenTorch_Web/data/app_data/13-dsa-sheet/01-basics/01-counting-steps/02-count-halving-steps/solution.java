public class Main {
    // O(1) time, O(1) space
    static long countHalvingSteps(long n) {
        return 63 - Long.numberOfLeadingZeros(n);
    }

    public static void main(String[] args) {
        System.out.println(countHalvingSteps(8L));
    }
}
