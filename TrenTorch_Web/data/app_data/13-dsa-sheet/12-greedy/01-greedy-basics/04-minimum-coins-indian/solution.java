public class Main {
    // O(1) time, O(1) space (fixed list of 9 denominations)
    static long fewestNotes(long amount) {
        long[] values = {2000L, 500L, 100L, 50L, 20L, 10L, 5L, 2L, 1L};
        long total = 0;
        for (long value : values) {
            total += amount / value;
            amount %= value;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(fewestNotes(70L));
    }
}
