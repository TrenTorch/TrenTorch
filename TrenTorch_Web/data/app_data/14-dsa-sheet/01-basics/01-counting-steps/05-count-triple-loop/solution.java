public class Main {
    // O(1) time, O(1) space
    static long countTripleLoop(long n) {
        return n * (n + 1) * (n + 2) / 6;
    }

    public static void main(String[] args) {
        System.out.println(countTripleLoop(3L));
    }
}
