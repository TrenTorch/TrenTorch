public class Main {
    // O(n log n) time, O(n) space (sorts copies of both arrays)
    static long assignCookies(long[] greed, long[] sizes) {
        long[] g = greed.clone();
        java.util.Arrays.sort(g);
        long[] s = sizes.clone();
        java.util.Arrays.sort(s);
        int child = 0;
        for (long cookie : s) {
            if (child < g.length && g[child] <= cookie) {
                child++;
            }
        }
        return child;
    }

    public static void main(String[] args) {
        System.out.println(assignCookies(new long[]{1L, 2L, 3L}, new long[]{1L, 1L}));
    }
}
