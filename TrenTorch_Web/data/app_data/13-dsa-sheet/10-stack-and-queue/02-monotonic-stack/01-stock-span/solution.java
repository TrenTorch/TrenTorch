public class Main {
    // O(n) time, O(n) space
    static long[] stockSpan(long[] prices) {
        long[] out = new long[prices.length];
        int[] stack = new int[prices.length];
        int top = 0;
        for (int i = 0; i < prices.length; i++) {
            long p = prices[i];
            while (top > 0 && prices[stack[top - 1]] <= p) {
                top--;
            }
            out[i] = top > 0 ? i - stack[top - 1] : i + 1;
            stack[top++] = i;
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(stockSpan(new long[]{100L, 80L, 60L, 70L, 60L, 75L, 85L})));
    }
}
