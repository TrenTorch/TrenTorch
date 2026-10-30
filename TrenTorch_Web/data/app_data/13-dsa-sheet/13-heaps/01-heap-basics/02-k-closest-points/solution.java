import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class Main {
    // Expected O(n + k log k) time, O(n) space
    static long[][] kClosest(long[][] points, long k) {
        if (k <= 0) return new long[0][];
        int need = (int) k;
        List<Item> pool = new ArrayList<>();
        for (long[] p : points) {
            pool.add(new Item(p));
        }
        if (need < pool.size()) {
            List<Item> chosen = new ArrayList<>();
            Random random = ThreadLocalRandom.current();
            while (need > 0) {
                Item pivot = pool.get(random.nextInt(pool.size()));
                List<Item> less = new ArrayList<>();
                List<Item> equal = new ArrayList<>();
                List<Item> greater = new ArrayList<>();
                for (Item item : pool) {
                    int cmp = compare(item, pivot);
                    if (cmp < 0) less.add(item);
                    else if (cmp == 0) equal.add(item);
                    else greater.add(item);
                }
                if (need <= less.size()) {
                    pool = less;
                } else if (need <= less.size() + equal.size()) {
                    chosen.addAll(less);
                    chosen.addAll(equal.subList(0, need - less.size()));
                    need = 0;
                } else {
                    chosen.addAll(less);
                    chosen.addAll(equal);
                    need -= less.size() + equal.size();
                    pool = greater;
                }
            }
            pool = chosen;
        }
        pool.sort(Comparator.comparingLong((Item i) -> i.dist)
                .thenComparingLong(i -> i.x)
                .thenComparingLong(i -> i.y));
        long[][] result = new long[pool.size()][2];
        for (int i = 0; i < pool.size(); i++) {
            result[i] = pool.get(i).point;
        }
        return result;
    }

    private static int compare(Item a, Item b) {
        if (a.dist != b.dist) return Long.compare(a.dist, b.dist);
        if (a.x != b.x) return Long.compare(a.x, b.x);
        return Long.compare(a.y, b.y);
    }

    private static class Item {
        long dist;
        long x;
        long y;
        long[] point;
        Item(long[] p) {
            this.x = p[0];
            this.y = p[1];
            this.dist = x * x + y * y;
            this.point = p;
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(kClosest(new long[][]{new long[]{1L, 3L}, new long[]{-2L, 2L}}, 1L)));
    }
}
