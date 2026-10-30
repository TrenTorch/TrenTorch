import java.util.Arrays;

public class Main {
    // O(k * E) time, O(n) space where E = flights.length
    static long cheapestPrice(long n, long[][] flights, long src, long dst, long k) {
        long INF = 1_000_000_000_000L;
        long[] best = new long[(int) n];
        Arrays.fill(best, INF);
        best[(int) src] = 0;
        for (int i = 0; i <= k; i++) {
            long[] nxt = best.clone();
            for (long[] flight : flights) {
                int a = (int) flight[0];
                int b = (int) flight[1];
                long price = flight[2];
                if (best[a] != INF && best[a] + price < nxt[b]) {
                    nxt[b] = best[a] + price;
                }
            }
            best = nxt;
        }
        return best[(int) dst] == INF ? -1 : best[(int) dst];
    }

    public static void main(String[] args) {
        System.out.println(cheapestPrice(4L, new long[][]{new long[]{0L, 1L, 100L}, new long[]{1L, 2L, 100L}, new long[]{2L, 0L, 100L}, new long[]{1L, 3L, 600L}, new long[]{2L, 3L, 200L}}, 0L, 3L, 1L));
    }
}
