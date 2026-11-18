import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Main {
    // O(n α(n)) time, O(n) space
    static long removeStones(long[][] stones) {
        Map<Long, Long> parent = new HashMap<>();
        Map<Long, Long> size = new HashMap<>();

        for (long[] stone : stones) {
            long x = stone[0];
            long y = stone[1] + 10001L; // offset to avoid collision between x and y coordinates

            long ra = find(x, parent, size);
            long rb = find(y, parent, size);

            if (ra != rb) {
                if (size.get(ra) < size.get(rb)) {
                    long temp = ra;
                    ra = rb;
                    rb = temp;
                }
                parent.put(rb, ra);
                size.put(ra, size.get(ra) + size.get(rb));
            }
        }

        Set<Long> groups = new HashSet<>();
        for (long[] stone : stones) {
            groups.add(find(stone[0], parent, size));
        }

        return (long) stones.length - groups.size();
    }

    private static long find(long a, Map<Long, Long> parent, Map<Long, Long> size) {
        if (!parent.containsKey(a)) {
            parent.put(a, a);
            size.put(a, 1L);
            return a;
        }
        while (parent.get(a) != a) {
            parent.put(a, parent.get(parent.get(a)));
            a = parent.get(a);
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(removeStones(new long[][]{new long[]{0L, 0L}, new long[]{0L, 1L}, new long[]{1L, 0L}, new long[]{1L, 2L}, new long[]{2L, 1L}, new long[]{2L, 2L}}));
    }
}
