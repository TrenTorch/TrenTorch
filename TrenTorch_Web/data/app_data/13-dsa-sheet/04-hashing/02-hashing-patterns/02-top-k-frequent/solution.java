import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class Main {
    // O(n) expected time, O(n) space
    static long[] topKFrequent(long[] nums, long k) {
        Map<Long, Integer> freq = new HashMap<>();
        for (long num : nums) {
            freq.merge(num, 1, Integer::sum);
        }

        List<Pair> pairs = new ArrayList<>(freq.size());
        for (Map.Entry<Long, Integer> entry : freq.entrySet()) {
            pairs.add(new Pair(-entry.getValue(), entry.getKey()));
        }

        if (k <= 0) {
            return new long[0];
        }

        int need = (int) k;
        if (need < pairs.size()) {
            List<Pair> chosen = new ArrayList<>(need);
            List<Pair> pool = pairs;
            Random random = new Random();

            while (need > 0) {
                Pair pivot = pool.get(random.nextInt(pool.size()));
                List<Pair> less = new ArrayList<>();
                List<Pair> greater = new ArrayList<>();

                for (Pair p : pool) {
                    int cmp = p.compareTo(pivot);
                    if (cmp < 0) {
                        less.add(p);
                    } else if (cmp > 0) {
                        greater.add(p);
                    }
                }

                if (need <= less.size()) {
                    pool = less;
                } else if (need == less.size() + 1) {
                    chosen.addAll(less);
                    chosen.add(pivot);
                    need = 0;
                } else {
                    chosen.addAll(less);
                    chosen.add(pivot);
                    need -= less.size() + 1;
                    pool = greater;
                }
            }
            pairs = chosen;
        }

        Collections.sort(pairs);
        long[] result = new long[pairs.size()];
        for (int i = 0; i < pairs.size(); i++) {
            result[i] = pairs.get(i).value();
        }
        return result;
    }

    // Pair ordered by (-count, value) so that the smallest pair corresponds to the most frequent value
    private static record Pair(long negCount, long value) implements Comparable<Pair> {
        @Override
        public int compareTo(Pair other) {
            int cmp = Long.compare(this.negCount, other.negCount);
            if (cmp != 0) return cmp;
            return Long.compare(this.value, other.value);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(topKFrequent(new long[]{1L, 1L, 1L, 2L, 2L, 3L}, 2L)));
    }
}
