public class Main {
    // O(n) time, O(1) space
    static long minCostClimbing(long[] cost) {
        long prev2 = 0;
        long prev1 = 0;
        for (int i = 2; i <= cost.length; i++) {
            long next = Math.min(prev1 + cost[i - 1], prev2 + cost[i - 2]);
            prev2 = prev1;
            prev1 = next;
        }
        return prev1;
    }

    public static void main(String[] args) {
        System.out.println(minCostClimbing(new long[]{10L, 15L, 20L}));
    }
}
