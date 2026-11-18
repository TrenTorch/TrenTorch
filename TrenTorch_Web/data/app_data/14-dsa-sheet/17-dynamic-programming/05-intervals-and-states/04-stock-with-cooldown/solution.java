public class Main {
    // O(n) time, O(1) space
    static long maxProfitCooldown(long[] prices) {
        long hold = Long.MIN_VALUE;
        long sold = 0;
        long rest = 0;
        for (long price : prices) {
            long newHold = Math.max(hold, rest - price);
            long newSold = hold + price;
            long newRest = Math.max(rest, sold);
            hold = newHold;
            sold = newSold;
            rest = newRest;
        }
        return Math.max(sold, rest);
    }

    public static void main(String[] args) {
        System.out.println(maxProfitCooldown(new long[]{1L, 2L, 3L, 0L, 2L}));
    }
}
